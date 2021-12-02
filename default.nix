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
      todonotes
      biblatex
      xcolor
      titlesec
      environ
      abstract
      cancel
      latexmk
      enumitem
      minted
      fvextra
      catchfile
      xstring
      koma-script
      framed
    ; });
in pkgs.stdenv.mkDerivation {
  pname = "phd-thesis";
  version = "0.0.1";
  src = ./.;
  buildInputs = [tex pkgs.python39Packages.pygments];
  phases = "buildPhase";
  buildPhase = ''
  ./build.sh
  '';
  # ${./.} is the path to /nix/store/... ${toString ./.} evaluates to
  # the current directory.
  LUA_PATH = "${toString ./.}/lua/?.lua;$LUA_PATH";
}
