#!/usr/bin/python3

"""
Example:
./jscope-uutpanel-gen.py $UUTS > ~/jScope/configurations/FLARE_2COL.jscp
"""

import MDSplus
import argparse
import os


def get_args():
    parser = argparse.ArgumentParser(description="jScope file creator.")
    parser.add_argument('--max_rows', default=8, type=int, help="max rows")
    parser.add_argument('--node', default="tr", type=str, help="top node")
    parser.add_argument('--nchan', default=1, type=int, help="channels per panel")
    parser.add_argument('uuts', nargs='+', help="uut list")
    return parser.parse_args()


def get_default_jscp():
    """
    Retrieves a default jscp file to use as a template.
    """
    user = os.getlogin()
    with open('/home/{}/jScope/configurations/default.jscp'.format(user)) as f:
        text = f.read()
    return text


def create_new_jscp(args, text):
    cols = 1
    rows = (len(args.uuts),0,)
    new_text = ""

    
    if len(args.uuts) > args.max_rows:
        cols = 2
        rows = (len(args.uuts)/2, len(args.uuts)//2,)

    text += "Scope.plot_1_1.num_shot: 1\n"

    text = text.replace("Scope.rows_in_column_2: 1",
                        "Scope.rows_in_column_2: {}".format(rows[1]))
    text = text.replace("Scope.rows_in_column_1: 1",
                        "Scope.rows_in_column_1: {}".format(rows[0]))
    text = text.replace("Scope.plot_1_1.num_expr: 0",
                        "Scope.plot_1_1.num_expr: 1")
    text = text.replace("Scope.plot_1_1.global_defaults: -1",
                        "Scope.plot_1_1.global_defaults: 196353")

    for line in text.split("\n"):
        if line.startswith("Scope.plot_1_1"):
            line_to_add = line.replace("1_1", "{index}_{column}")
            new_text += line_to_add + "\n"

    row = 1
    col = 1
    for id, uut in enumerate(args.uuts):
        if id == rows[0]:
            row = 1
            col = 2

        if id != 0:
            text += new_text.format(index=row, column=col)
        text += "Scope.plot_{}_{}.title: '{} shot: '//$SHOT\n".format(
            row, col, uut.upper())
        text += "Scope.plot_{}_{}.experiment: {}\n".format(row, col, uut.upper())
        text += "Scope.plot_{}_{}.num_expr: {}\n".format(row, col, args.nchan)
        for ch in range(1,args.nchan+1):
            text += "Scope.plot_{}_{}.y_expr_{}: \TOP:{}:INPUT_{:03d}\n".format(row, col, ch, args.node, ch)
            text += "Scope.plot_{}_{}.color_1_1: {}\n".format(row, col, ch)
            text += "Scope.plot_{}_{}.mode_1D_1_1: Line\n".format(row, col)
            text += "Scope.plot_{}_{}.mode_2D_1_1: xz(y)\n".format(row, col)
            text += "Scope.plot_{}_{}.marker_1_1: 0\n".format(row, col)
            text += "Scope.plot_{}_{}.step_marker_1_1: 1\n\n".format(row, col)
        row += 1
    print(text)
    return None


def main():
    args = get_args()
    text = get_default_jscp()
    create_new_jscp(args, text)


if __name__ == '__main__':
    main()
