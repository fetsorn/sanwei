{
  inputs = { nixpkgs.url = "github:nixos/nixpkgs/nixos-22.11"; };
  outputs = inputs@{ nixpkgs, ... }:
    let
      eachSystem = systems: f:
        let
          op = attrs: system:
            let
              ret = f system;
              op = attrs: key:
                let
                  appendSystem = key: system: ret: { ${system} = ret.${key}; };
                in attrs // {
                  ${key} = (attrs.${key} or { })
                    // (appendSystem key system ret);
                };
            in builtins.foldl' op attrs (builtins.attrNames ret);
        in builtins.foldl' op { } systems;
      defaultSystems = [ "x86_64-linux" "aarch64-darwin" ];
    in eachSystem defaultSystems (system:
      let
        pkgs = import nixpkgs { inherit system; };

        pkgs-x86_64 = import inputs.nixpkgs { system = "x86_64-darwin"; };

        app = pkgs.stdenv.mkDerivation {
          name = "sanwei";

          src = ./.;

          buildPhase = ''
            ${pkgs-x86_64.blender} \
              --background \
              --python ./text.py \
              --render-frame 1 \
              -- ./output.png 100 128 "你好"
          '';

          installPhase = "cp ./output.png $out";
        };

        script = pkgs.writeShellScriptBin "serve" ''
          ${pkgs.blender} \
            --background \
            --python ${./text.py} \
            --render-frame 1
        '';
      in rec {
        packages = { inherit app script; };

        defaultPackage = script;

        defaultApp = {
          type = "app";
          program = "${script}/bin/serve";
        };

        devShell =
          pkgs.mkShell { nativeBuildInputs = with pkgs-x86_64; [ blender ]; };
      });
}
