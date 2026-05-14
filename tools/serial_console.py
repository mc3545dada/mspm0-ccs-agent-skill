#!/usr/bin/env python3
"""Small serial console for MSPM0 UART smoke tests."""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime

try:
    import serial
    import serial.tools.list_ports
except ImportError as exc:
    raise SystemExit(
        "pyserial is required. Install it with: python -m pip install pyserial"
    ) from exc


def list_ports() -> int:
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("No serial ports found.")
        return 1
    for port in ports:
        print(f"{port.device}\t{port.description}\t{port.hwid}")
    return 0


def format_bytes(data: bytes, *, as_hex: bool, encoding: str) -> str:
    if as_hex:
        return " ".join(f"{byte:02X}" for byte in data)
    return data.decode(encoding, errors="replace")


def timestamp_prefix() -> str:
    now = datetime.now()
    return f"[{now:%H:%M:%S}.{now.microsecond // 1000:03d}]"


def open_serial(args: argparse.Namespace) -> serial.Serial:
    return serial.Serial(
        port=args.port,
        baudrate=args.baudrate,
        bytesize=args.bytesize,
        parity=args.parity,
        stopbits=args.stopbits,
        timeout=args.timeout,
        write_timeout=args.write_timeout,
        rtscts=args.rtscts,
        dsrdtr=args.dsrdtr,
        xonxoff=args.xonxoff,
    )


def run_console(args: argparse.Namespace) -> int:
    start = time.monotonic()
    received = 0

    try:
        with open_serial(args) as ser:
            print(
                f"Opened {ser.port} at {ser.baudrate} "
                f"{ser.bytesize}{ser.parity}{ser.stopbits}"
            )

            if args.send is not None:
                payload = args.send.encode(args.encoding)
                if args.append_newline:
                    payload += b"\n"
                ser.write(payload)
                ser.flush()
                print(f"TX {len(payload)} bytes")

            while True:
                if args.duration is not None and time.monotonic() - start >= args.duration:
                    break

                data = ser.read(args.chunk_size)
                if not data:
                    continue

                received += len(data)
                text = format_bytes(data, as_hex=args.hex, encoding=args.encoding)
                if args.timestamp:
                    prefix = timestamp_prefix()
                    print(f"{prefix} {text}", end="" if not args.hex else "\n")
                else:
                    print(text, end="" if not args.hex else "\n")
                sys.stdout.flush()

    except serial.SerialException as exc:
        print(f"Serial error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print()

    if args.duration is not None:
        print(f"\nDone. RX {received} bytes.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read and write a UART serial port.")
    parser.add_argument("--list", action="store_true", help="List available serial ports and exit.")
    parser.add_argument("-p", "--port", help="Serial port, such as COM6.")
    parser.add_argument("-b", "--baudrate", type=int, default=115200, help="Baud rate. Default: 115200.")
    parser.add_argument("--bytesize", type=int, default=8, choices=(5, 6, 7, 8), help="Data bits. Default: 8.")
    parser.add_argument("--parity", default="N", choices=("N", "E", "O", "M", "S"), help="Parity. Default: N.")
    parser.add_argument("--stopbits", type=float, default=1, choices=(1, 1.5, 2), help="Stop bits. Default: 1.")
    parser.add_argument("--timeout", type=float, default=0.2, help="Read timeout seconds. Default: 0.2.")
    parser.add_argument("--write-timeout", type=float, default=1.0, help="Write timeout seconds. Default: 1.0.")
    parser.add_argument("--duration", type=float, help="Read duration seconds. Omit to read until Ctrl+C.")
    parser.add_argument("--chunk-size", type=int, default=128, help="Read chunk size. Default: 128.")
    parser.add_argument("--encoding", default="utf-8", help="Text encoding. Default: utf-8.")
    parser.add_argument("--hex", action="store_true", help="Print received bytes as hex.")
    parser.add_argument("--timestamp", action="store_true", help="Prefix received data with local timestamps.")
    parser.add_argument("--send", help="Text to send after opening the port.")
    parser.add_argument("--append-newline", action="store_true", help="Append LF to --send payload.")
    parser.add_argument("--rtscts", action="store_true", help="Enable RTS/CTS flow control.")
    parser.add_argument("--dsrdtr", action="store_true", help="Enable DSR/DTR flow control.")
    parser.add_argument("--xonxoff", action="store_true", help="Enable software flow control.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.list:
        return list_ports()
    if not args.port:
        parser.error("--port is required unless --list is used")
    return run_console(args)


if __name__ == "__main__":
    raise SystemExit(main())
