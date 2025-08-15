{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python312
    python312Packages.requests
    python312Packages.types-requests
    python312Packages.lxml
    python312Packages.lxml-stubs
    python312Packages.influxdb-client
    ruff
  ];
}

