{
  description = "Pelican blog development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = { nixpkgs, ... }:
    let
      forAllSystems = nixpkgs.lib.genAttrs [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
    in {
      devShells = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python3.withPackages (ps: with ps; [
            pelican
            markdown
            typogrify
            ghp-import
            webassets
            cssmin
            fabric
            jinja2
            markupsafe
            css-html-js-minify
          ]);
        in {
          default = pkgs.mkShell {
            packages = [
              python
              pkgs.gnumake
            ];
          };
        }
      );
    };
}
