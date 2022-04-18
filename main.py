from sqlite3 import connect
from utils import Utils
import re

tools = Utils()

f = open("Ore no kurasu ni wakagaetta motoyome ga iru.tex", "w", encoding='utf-8')
f.writelines("""
\\documentclass[12pt,a4paper, twosides]{book}
% \\usepackage[left=20mm, right=20mm, top=1in, bottom=1.1in]{geometry}
\\usepackage[utf8]{inputenc}
\\usepackage[utf8]{vietnam}
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usepackage{fancyhdr}
\\usepackage{fontspec}
\\usepackage{amsfonts}
\\usepackage{hyperref}
\\usepackage{graphicx}
\\usepackage[utf8]{inputenc}
\graphicspath{ {./images/} }

% \\DeclareUnicodeCharacter{300C}{$\\lfloor$}
% \\DeclareUnicodeCharacter{300D}{$\\rceil$}
% \\DeclareUnicodeCharacter{25C6}{$\\mathbin{\\blacklozenge}$}
% \\DeclareUnicodeCharacter{30FB}{$\\cdot$}
\\newcommand*{\\mysymb}[1]{{\\fontspec{Droid Sans Fallback}\\symbol{#1}}}


\\pagestyle{plain}
\\fancyfoot[RE,LO]{\\thepage}

\\begin{document}
""")

regex = re.compile(r"(\[note[0-9]*\])")

for chapter_id in range(0, tools.get_number_of_chapters()):
# chapter_id = 3
    print(f"Reading chapter {chapter_id}")
    chapter = tools.get_content_chapter(chapter_id)
    f.writelines("""
    \\begin{center}
    \\textbf{\\large """ + tools.get_title_chapter(chapter_id).replace('-', '\\\\') + """}
    \\end{center}
    """)
    f.write("\\noindent\n")
    for line in chapter:
        content = line.contents[0]
        try:
            url = content["src"]
            name = content["alt"]
            content.has_attr("src")
            # print(url, name)
            # tools.down_load_img(url, f"assets/{name}")
            f.write("\\begin{center}\n")
            f.write(f"\\includegraphics[width=0.5\textwidth]{{assets/{name}}}\n")
            f.write("\\end{center}\n")

        except:
            content = content.replace('\u200e', '')
            content = content.replace('&', "\\&")
            content = content.replace('^', '\\^')
            content = content.replace('_', "\\_")
            content = content.replace('\u3010', "\\mysymb{\"3010}")
            content = content.replace('\u3011', "\\mysymb{\"3011}")
            content = content.replace('\u300c', "$\\lfloor$")
            content = content.replace('\u300d', "$\\rceil$")
            content = content.replace('\u25c6', "$\\mathbin{\\blacklozenge}$")
            content = content.replace('\u30fb', "$\\cdot$")

            content = regex.sub(r"$^\\text{\1}$", content)
            if content == "Đọc bản dịch gốc và ủng hộ nhóm dịch tại ":
                content += "\\href{https://ln.hako.re/}{ln.hako.re}"
            f.write(content)
            f.write('\\\\')
            f.write('\n')
    f.write("\\newpage\n")

f.write("\\end{document}")