from collections import defaultdict
import argparse
import os
import re


# http://xpo6.com/download-stop-word-list/  2020-08-23
STOPWORDS = 'a able about across after all almost also am among an and any are as at be because been but by can ' \
            'cannot could dear did do does either else ever every for from get got had has have he her hers him his ' \
            'how however i if in into is it its just least let like likely may me might most must my neither no nor ' \
            'not of off often on only or other our own rather said say says she should since so some than that the ' \
            'their them then there these they this tis to too twas us wants was we were what when where which while ' \
            'who whom why will with would yet you your'.split()

CUTOFF = 10


def text2words(text):
    txt = text.lower()
    txt = txt.replace("'s", '')
    # txt = re.sub(r'[^\w\s\r\n]','', txt)
    txt = re.sub(r'[^\w\s]','', txt)
    return txt.split()

def freq_dist(txt, ignore_list=None):
    _word_counts = defaultdict(int)
    _word_list = text2words(txt)
    if ignore_list:
        _word_list = [w for w in _word_list if w not in ignore_list]
    for w in _word_list:
        _word_counts[w] += 1
    return _word_counts


def process_path(pth, cutoff=CUTOFF, ignore_list=None):

    word_counts = defaultdict(int)
    in_files = defaultdict(list)

    sentences = {}
    il = STOPWORDS
    if ignore_list:
        il.extend(ignore_list)
    for fname in os.listdir(pth):
        filename = os.path.join(pth, fname)
        with open(filename, 'r') as f:
            _text = f.read()
        _text = re.sub(r'[\n\r]+', '', _text)
        freq = freq_dist(_text, ignore_list=il)

        for w, c in freq.items():
            in_files[w].append(fname)
            # store
            word_counts[w] += c

        # break text

        cleaner_text = re.sub(r'([\!\.\?]+)', r'\1 ', _text).replace('  ', ' ')
        sentences[fname] = re.split(r'[\!\.\?]+(\s|$)', cleaner_text)

    sorted_freq = sorted(word_counts.items(), key=lambda kv: kv[1])
    sorted_freq = [(x, y) for x, y in sorted_freq if y >= cutoff]
    sorted_freq.reverse()
    output = []
    for w, c in sorted_freq:
        fnames = in_files[w]
        row = [w, c, fnames]
        patt = re.compile(r'(\s|^)(%s)($|\s)' % re.escape(w), re.IGNORECASE)
        matches = []
        for fn in fnames:
            for sentence in sentences[fn]:
                repl, cnt = patt.subn(r'\1<b>\2</b>\3', sentence)
                if cnt > 0:
                    matches.append(repl)
        row.append(matches)
        output.append(row)
    return output



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Calculate word frequency distribution from text files in a named folder')
    parser.add_argument('path', metavar='path', type=str,
                        help='relative or absolute path of folder containg text files')
    parser.add_argument('-c', '--cutoff', dest='cutoff', type=int,
                        default=CUTOFF,
                        help='Disregard counts below this number')
    parser.add_argument('-i', '--ignore', dest='ignore_list', nargs='+', type=str, default=[],
                        help='Words to ignore')
    parser.add_argument('-o', '--output', dest='output', type=str, default='freq_dist.html',
                        help='HTML file name')

    args = parser.parse_args()
    if os.path.isdir(args.path):
        result = process_path(args.path, cutoff=args.cutoff, ignore_list=args.ignore_list)
    output = """
    <html>
        <head>
            <title>Word frequency distribution</title>
            <style>
                td { vertical-align: top }
            </style>
        </head>
        <body>
        <h1>Word Frequency Distribution</h1>
        <h3>Document path: %s</h3>
        <table>
            <thead>
                <tr><th>Word(total occurrences)</th><th>Documents</th><th>Sentences containing the word</th></tr>
            </thead>
            <tbody>""" % args.path
    for w, c, docs, xcerpts in result:
        output += '<tr><td>%s (%s)</td><td>%s</td><td>%s</td></tr>\n' % (
            w.title(), c, ', '.join(docs), '\n'.join(['<p>%s</p>' % p for p in xcerpts])
        )
    output += """
    </tbody>
    </table>
    </body>
    </html>
    """
    with open(args.output, 'w') as f:
        f.write(output)
    print('Wrote %s' % args.output)


