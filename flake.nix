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
      defaultSystems = [ "x86_64-linux" "aarch64-darwin" "x86_64-darwin" ];
    in eachSystem defaultSystems (system:
      let
        pkgs = import nixpkgs { inherit system; };

        bpy-src = {
          "x86_64-linux" = {
            sha256 = ""; # TODO
            platform = "manylinux_2_28_x86_64";
          };
          "aarch64-darwin" = {
            sha256 = "sha256-MgZELnF56RztfJ0vVqTFDE5Gpeq0Gaz+NfnEP3nPqPE=";
            platform = "macosx_11_0_arm64";
          };
          "x86_64-darwin" = {
            sha256 = ""; # TODO
            platform = "macosx_10_15_x86_64";
          };
        };

        bpy = pkgs.python310Packages.buildPythonPackage rec {
          pname = "bpy";
          version = "3.5.0";
          format = "wheel";
          src = pkgs.python310Packages.fetchPypi rec {
            inherit pname version format;
            sha256 = bpy-src.${system}.sha256;
            dist = python;
            python = "cp310";
            abi = "cp310";
            platform = bpy-src.${system}.platform;
          };
          propagatedBuildInputs = with pkgs.python310Packages; [
            numpy
            zstandard
            cython
            requests
          ];
        };

        sanwei = pkgs.python310Packages.buildPythonPackage rec {
          name = "sanwei";
          format = "pyproject";
          src = ./.;
          propagatedBuildInputs = [ pkgs.python310Packages.hatchling bpy ];
          meta = { mainProgram = "sanwei"; };
        };

        # arm64 macos requires global installation of Blender
        blender-binary = if system == "aarch64-darwin" then
          "/Applications/Blender.app/Contents/MacOS/Blender"
        else
          "${pkgs.blender}/bin/blender";

        image = pkgs.stdenv.mkDerivation {
          name = "sanwei";

          src = ./.;

          buildPhase = ''
            ${sanwei}/bin/sanwei --output ./output \
                                 --binary ${blender-binary} \
                                 --font-path "${pkgs.wqy_zenhei}/share/fonts/wqy-zenhei.ttc" \
                                 --font-name "WenQuanYi Zen Hei Regular"
          '';

          installPhase = "cp output.png $out";
        };

        imagedir = pkgs.stdenv.mkDerivation {
          name = "sanwei";

          src = ./.;

          buildPhase = ''
            ${sanwei}/bin/sanwei --sanwei-output ./output
            export hash=$(sha256sum ./output.png | cut -c 1-64)
            mv output.png $hash.png;
          '';

          installPhase = "mkdir $out; cp *.png $out";
        };
      in rec {
        packages = { inherit sanwei image imagedir; };

        defaultPackage = sanwei;

        defaultApp = sanwei;

        devShell = pkgs.mkShell {
          nativeBuildInputs = with pkgs; [ blender wqy_zenhei python310 ];
        };
      });
}
