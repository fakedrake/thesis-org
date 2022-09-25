{ pkgs ? import <nixpkgs> {}} :
let
  dot2tex = pkgs.python2Packages.dot2tex;
  tectonic_5 = pkgs.callPackage ./tectonic_pkg.nix {
    rustPlatform = pkgs.rustPackages.rustPlatform;
    harfbuzz = pkgs.harfbuzzFull;
  };
  lua = pkgs.luaPackages.luaposix;
  tex = with pkgs; (texlive.combine {
    inherit (texlive)
      scheme-small
      enumitem
      mdframed
        needspace
        zref
      biblatex
      xcolor
      tcolorbox
      titlesec
      adjustbox
      collectbox
      emoji
      datetime2
      etoolbox
      tracklang
      environ
      abstract
      cancel
      latexmk
      minted
      fvextra
      catchfile
      xstring
      koma-script
      framed
    ; });
  py = pkgs.python39.withPackages (p: with p; [pandas numpy pygments matplotlib]);
  # py = pkgs.python39.withPackages (p: with p; []);
in pkgs.stdenv.mkDerivation {
  pname = "phd-thesis";
  version = "0.0.1";
  src = ./.;
  buildInputs = [tex py];
  phases = "buildPhase";
  buildPhase = ''
  ./build.sh
  '';
  # ${./.} is the path to /nix/store/... ${toString ./.} evaluates to
  # the current directory.
  LUA_PATH = "${toString ./.}/lua/?.lua;$LUA_PATH";

}
