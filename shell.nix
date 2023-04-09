{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "chess with qt gui";
  buildInputs = with pkgs; [
    gh
    qt6.full
    (python3.withPackages (ps: with ps; with python3Packages; [
      jupyter
      ipython
      ipykernel
      pyqt6
    ]))
  ];
  shellHook = ''
    echo "$succesfully launched shell";
  '';
}
