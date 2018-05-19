import codecs, json, os, markdown, csv, re, shutil
from StringIO import StringIO
from datetime import datetime

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = f

    def __iter__(self):
        return self

    def next(self):
        val = self.reader.next()
        raw = val.encode("utf-8")
        if raw.startswith(codecs.BOM_UTF8):
            raw = raw.replace(codecs.BOM_UTF8, '', 1)
        return raw

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class BuildException(Exception):
    pass

class Command(object):
    def __init__(self, raw, file_cfg, config):
        self.config = config
        self.file_cfg = file_cfg

        raw = raw.strip()
        raw = raw.replace("\n", " ").strip()
        boundary = raw.find(" ")
        args = []
        if boundary == -1:
            self.command = raw
        else:
            self.command = raw[:boundary].strip()
            sargs = StringIO(raw[boundary:])
            args = UnicodeReader(sargs).next()

        def listify(val):
            if "|" in val:
                vals = [v.strip() for v in val.split("|")]
                val = vals
            return val

        self.args = []
        self.kwargs = {}
        for arg in args:
            if "=" in arg:
                bits = arg.split("=")
                val = listify(bits[1].strip())
                self.kwargs[bits[0].strip()] = val
            else:
                val = listify(arg.strip())
                self.args.append(arg.strip())

    def run(self):
        return COMMANDS[self.command](self.file_cfg, self.config, *self.args, **self.kwargs)

    def _parse(self, raw):
        pass

def run(config):
    bd = config.get("build_dir")
    od = config.get("out_dir")
    shutil.rmtree(bd)
    shutil.rmtree(od)
    os.mkdir(bd)
    os.mkdir(od)

    expand_dir = os.path.join(bd, "expand")
    number_dir = os.path.join(bd, "number")
    integrate_dir = os.path.join(bd, "integrate")
    if not os.path.exists(expand_dir):
        os.mkdir(expand_dir)
    if not os.path.exists(number_dir):
        os.mkdir(number_dir)
    if not os.path.exists(integrate_dir):
        os.mkdir(integrate_dir)

    files = config.get("files", [])
    for file_cfg in files:
        if file_cfg.get("process", False):

            of = file_cfg.get("out")
            out = os.path.join(od, of)
            text = build(file_cfg, config)
            with codecs.open(out, "wb", "utf-8") as f:
                f.write(text)
        else:
            _unprocessed_entry(file_cfg, config)


def _unprocessed_entry(file_cfg, config):
    src_dir = config.get("src_dir")
    out_dir = config.get("out_dir")
    root = file_cfg.get("root")
    out_file = file_cfg.get("out")
    root_dir = file_cfg.get("root_dir")
    file_out_dir = file_cfg.get("out_dir")

    if root is not None:
        out = os.path.join(out_dir, out_file)
        infile = os.path.join(src_dir, root)
        shutil.copy(infile, out)
    elif root_dir is not None:
        indir = os.path.join(src_dir, root_dir)
        out = os.path.join(out_dir, file_out_dir)
        shutil.copytree(indir, out)


def build(file_cfg, config, phases=None):
    if phases is None:
        phases = file_cfg.get("phases", ["expand", "number", "integrate", "render"])
    src_dir = config.get("src_dir")
    root = file_cfg.get("root")
    root = os.path.join(src_dir, root)

    if "expand" in phases:
        text = expand(root, file_cfg, config)
        fn = file_cfg.get("root").replace("/", "_")
        with codecs.open(os.path.join(config.get("build_dir"), "expand", fn), "wb", "utf-8") as f:
            f.write(text)
    if "number" in phases:
        text = index(text, file_cfg, config)
        fn = file_cfg.get("root").replace("/", "_")
        with codecs.open(os.path.join(config.get("build_dir"), "number", fn), "wb", "utf-8") as f:
            f.write(text)
    if "integrate" in phases:
        text = integrate(text, file_cfg, config)
        fn = file_cfg.get("root").replace("/", "_")
        with codecs.open(os.path.join(config.get("build_dir"), "integrate", fn), "wb", "utf-8") as f:
            f.write(text)
    if "render" in phases:
        text = render(text, file_cfg, config)

    return text + "\n\n"

def expand(path, file_cfg, config):
    out = ""
    with codecs.open(path, "rb", "utf-8") as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if line == "":
                return out
            if line.startswith("{%"):
                current_i = i
                line, i = _read_command(i, line, lines)
                command = Command(line, file_cfg, config)
                if command.command in EXPAND_COMMANDS:
                    out += command.run()
                else:
                    i = current_i
                    line = lines[i]
                    out += line
            else:
                out += line
            i += 1
    return out


def index(text, file_cfg, config):
    # now number the sections
    numbered = ""
    toc = {}
    lines = text.split("\n")
    for line in lines:
        if line.startswith("#"):
            num, newline = _number_header(line, file_cfg, config)
            if num is not None:
                toc[num] = _extract_title(line)
            line = newline
        numbered += line + "\n"
    file_cfg["toc"] = toc
    return numbered

def _extract_title(line):
    line = line.lstrip("#")
    line = line.strip()
    return line

def _read_command(idx, first_line, lines):
    command = first_line.strip()
    while not command.endswith("%}"):
        idx += 1
        command += " " + lines[idx].strip()
    return command[2:-2].strip(), idx

def _number_header(line, file_cfg, config):
    level = 0
    for c in line:
        if c == "#":
            level += 1
        else:
            break

    if "current_header" not in file_cfg:
        file_cfg["current_header"] = [0,0,0]
    current_header = file_cfg.get("current_header")

    if "toc" not in file_cfg:
        file_cfg["toc"] = {}

    if level == 0:
        return None, line
    elif level == 1:
        current_header[0] += 1
        current_header[1] = 0
        current_header[2] = 0
    elif level == 2:
        current_header[1] += 1
        current_header[2] = 0
    elif level == 3:
        current_header[2] += 1
    else:
        return None, line

    num = ""
    for x in current_header:
        if x > 0:
            num += str(x) + "."

    anchor = '<a name="' + num + '"></a>'
    return num, anchor + "\n" + "#" * level + " " + num + " " + line[level:].strip()

def integrate(text, file_cfg, config):
    cmd_rx = "(\{%.+?%\})"
    m = re.search(cmd_rx, text, re.DOTALL)
    while m is not None:
        matched = m.group(0)
        command = Command(matched[2:-2].strip(), file_cfg, config)
        rep = command.run()
        text = text.replace(matched, rep)
        m = re.search(cmd_rx, text, re.DOTALL)
    return text

def render(text, file_cfg, config):
    # first do a full markdown render
    body = markdown.markdown(text, extensions=["markdown.extensions.tables", "markdown.extensions.fenced_code"])

    # now clean up any unnecessary para tags before the html functions are run
    para_rxs = [("<p>\{~", "{~"), ("~\}</p>", "~}")]
    for rx in para_rxs:
        body = re.sub(rx[0], rx[1], body)

    cmd_rx = "(\{~.+?~\})"
    m = re.search(cmd_rx, body, re.DOTALL)
    while m is not None:
        matched = m.group(0)
        command = Command(matched[2:-2].strip(), file_cfg, config)
        rep = command.run()
        body = body.replace(matched, rep)
        m = re.search(cmd_rx, body, re.DOTALL)

    header = file_cfg.get("header")
    footer = file_cfg.get("footer")
    bd = config.get("src_dir")

    head = ""
    foot = ""

    if header is not None:
        head_path = os.path.join(bd, header)
        with codecs.open(head_path, "rb", "utf-8") as f:
            head = f.read()

    if footer is not None:
        foot_path = os.path.join(bd, footer)
        with codecs.open(foot_path, "rb", "utf-8") as f:
            foot = f.read()

    return head + body + foot


##################################################
# Commands

def include(file_cfg, config, path):
    nfc = {"root" : path}
    if "current_header" in file_cfg:
        nfc["current_header"] = file_cfg["current_header"]
    text = build(nfc, config, phases=["expand"])
    if "current_header" in file_cfg:
        file_cfg["current_header"] = nfc["current_header"]
    return text

def date(file_cfg, config, thedate, format):
    dv = None
    if thedate == "now":
        dv = datetime.utcnow()

    if dv is not None:
        return dv.strftime(format)

    raise BuildException()

def ref(file_cfg, config, reference):
    ref_file = config.get("resources", {}).get("ref")
    with codecs.open(ref_file, "rb", "utf-8") as f:
        reader = UnicodeReader(f)
        for row in reader:
            if row[0] == reference:
                return "[[" + row[0] + "](#" + _anchor_name(row[0]) + ")]"

    raise BuildException()

def table_rows_as_paras(file_cfg, config, source, links=None, bold=None, anchor=None):
    bd = config.get("src_dir")
    path = os.path.join(bd, source)
    paras = []
    with codecs.open(path, "rb", "utf-8") as f:
        reader = UnicodeReader(f)
        headers = reader.next()
        for row in reader:
            para = ""
            for i in range(len(row)):
                col = row[i]
                name = headers[i]

                a = ""
                if name == anchor and anchor is not None:
                    a = '<a name="' + _anchor_name(col) + '">'

                if name == links and links is not None:
                    col = "[" + col + "](" + col + ")"
                if name == bold and bold is not None:
                    col = "**" + col + "**"

                para += a + col + " "
            paras.append(para)
    return "\n\n".join(paras)

def dl(file_cfg, config, source, term, definition, link=None, size=None, offset=0):
    bd = config.get("src_dir")
    path = os.path.join(bd, source)
    frag = "<dl>"
    offset = int(offset)
    if size is not None:
        size = int(size)

    with codecs.open(path, "rb", "utf-8") as f:
        reader = UnicodeReader(f)
        headers = reader.next()

        n = 0
        for row in reader:
            if size is not None and n >= size + offset:
                break
            n += 1
            if n < offset + 1:
                continue

            dt = None
            dd = None
            a = ""
            for i in range(len(row)):
                col = row[i]
                name = headers[i]
                if name == term:
                    a = '<a name="' + _anchor_name(col) + '"></a>'
                if name == link:
                    col = "[" + col + "](" + col + ")"
                if name == term:
                    dt = col
                    continue
                if name == definition:
                    dd = col
                    continue
            dt = markdown.markdown(dt)[3:-4]    # removes the <p> and </p> markdown inserts
            dd = markdown.markdown(dd)[3:-4]    # removes the <p> and </p> markdown inserts
            frag += "<dt>" + a + dt + "</dt><dd>" + dd + "</dd>"

    frag += "</dl>"
    return frag

def table(file_cfg, config, source):
    bd = config.get("src_dir")
    path = os.path.join(bd, source)
    frag = ""
    with codecs.open(path, "rb", "utf-8") as f:
        reader = UnicodeReader(f)
        headers = reader.next()
        frag = "| " + " | ".join(headers) + " |\n"
        frag += "| " + "--- |" * len(headers) + "\n"
        for row in reader:
            linified_row = [cell.replace("\n", "<br>") for cell in row]
            frag += "| " + " | ".join(linified_row) + " |\n"
    return frag


def openapi_list_descriptions(file_cfg, config, source, field, keys=None):
    bd = config.get("src_dir")
    path = os.path.join(bd, source)
    frag = ""
    with codecs.open(path, "rb", "utf-8") as f:
        api = json.loads(f.read())
        bits = field.split(".")
        for bit in bits:
            api = api.get(bit)
        if keys is not None:
            if not isinstance(keys, list):
                keys = [keys]
            for key in keys:
                desc = api.get(key).get("description")
                frag += " * " + desc + "\n"
    return frag

def url(file_cfg, config, relpath):
    base = config.get("base_url")
    return base + relpath


def http_exchange(file_cfg, config, source, method, url, response, include_headers=None):
    bd = config.get("src_dir")
    path = os.path.join(bd, source)
    if include_headers is not None:
        if not isinstance(include_headers, list):
            include_headers = [include_headers]

    frag = method.upper() + " " + url + " HTTP/1.1\n"
    with codecs.open(path, "rb", "utf-8") as f:
        api = json.loads(f.read())
        paths = api.get("paths")
        path = paths.get(url)
        request = path.get(method)

        headers = [p for p in request.get("parameters", []) if p.get("in") == "header"]
        if include_headers is not None:
            headers = [h for h in headers if h.get("name") in include_headers]
        for h in headers:
            frag += h.get("name") + ": ...\n"

        frag += "\n\n"

        frag += "HTTP/1.1 " + response + "\n"
        resp = request.get("responses", {}).get(response)
        cts = resp.get("content", {}).keys()
        if len(cts) > 0:
            frag += "Content-Type: " + cts[0] + "\n"
        frag += "\n"
        frag += "[" + resp.get("description", "Empty Body") + "]\n"

    return frag


def openapi_paths(file_cfg, config, source, path_order=None, method_order=None, header_depth=1, omit=None, in_brief=None):
    if method_order is None:
        method_order = ["get", "post", "put", "delete"]
    header_depth = int(header_depth)
    bd = config.get("src_dir")
    path = os.path.join(bd, source)
    frag = ""
    with codecs.open(path, "rb", "utf-8") as f:
        api = json.loads(f.read())
        paths = api.get("paths")
        path_names = paths.keys()
        if path_order is not None:
            path_names = ["/" + po for po in path_order]
        for pn in path_names:
            path_info = paths.get(pn)
            if path_info is None:
                continue
            for method in method_order:
                method_info = path_info.get(method)
                if method_info is None:
                    continue
                frag += _render_method_info(header_depth, pn, method, method_info, omit, in_brief)
    return frag

def _render_method_info(header_depth, path_name, method, method_info, omit=None, in_brief=None):
    frag = "#" * header_depth + method.upper() + " " + path_name[1:] + "\n\n"
    frag += "{~ html div,clazz=openapi ~}\n"
    frag += method_info.get("summary", "") + "\n\n"
    frag += "**Headers**\n\n"

    for param in method_info.get("parameters", []):
        if param.get("in") != "header":
            continue
        frag += " * " + param.get("name") + "\n"
    frag += "\n"

    rb = method_info.get("requestBody")
    if rb is not None:
        frag += "**Body**\n\n"
        frag += rb.get("description", "") + "\n\n"

    frag += "**Responses**\n\n"

    frag += "| Code | Description |\n"
    frag += "| ---- | ----------- |\n"
    codes = method_info.get("responses", [])
    keys = codes.keys()
    keys = sorted(keys)
    for code in keys:
        if code in omit:
            continue
        if code in in_brief:
            code_info = codes.get(code)
            frag += "| " + code + " | " + code_info.get("description", "") + " |\n"
        else:
            code_info = codes.get(code)
            frag += "| " + code + " | " + code_info.get("description", "") + "<br><br>"

            headers = code_info.get("headers", [])
            if len(headers) > 0:
                frag += "**Headers**"
                frag += "<ul>"
                for header, hobj in headers.iteritems():
                    frag += "<li>" + header + " - " + hobj.get("description") + "</li>"
                frag += "</ul>"

            frag += "**Body**<ul>"
            content = code_info.get("content", [])
            if len(content) > 0:
                for ct, cobj in content.iteritems():
                    ct = ct.replace("*", "\*")
                    frag += "<li>" + ct + "</li>"
            else:
                frag += "<li>None</li>"
            frag += "</ul> |\n"

    frag += "\n{~ html /div ~}"
    return frag + "\n\n"

def aggregated_requirements(file_cfg, config, sources=None, order=None):
    if not isinstance(sources, list):
        sources = [sources]
    bd = config.get("src_dir")
    requirements = {}
    for source in sources:
        path = os.path.join(bd, source)
        with codecs.open(path, "rb", "utf-8") as f:
            reader = UnicodeReader(f)
            headers = reader.next()
            for header in headers:
                if header not in requirements:
                    requirements[header] = []
            for row in reader:
                for i in range(len(row)):
                    if row[i] == "":
                        continue
                    if row[i] not in requirements[headers[i]]:
                        requirements[headers[i]].append(row[i])

    if order is None:
        order = requirements.keys()

    frag = ""
    for key in order:
        reqs = requirements[key]
        frag += "**" + key + "**\n\n"
        for req in reqs:
            frag += " * " + req.replace("\n", "<br>") + "\n"
        frag += "\n"
    return frag

def content_disposition(file_cfg, config, reqs, hierarchy, groups, match):
    bd = config.get("src_dir")
    reqs_path = os.path.join(bd, reqs)
    hierarchy_path = os.path.join(bd, hierarchy)

    headers = []
    requirements = []
    with codecs.open(reqs_path, "rb", "utf-8") as f:
        reqs_reader = UnicodeReader(f)
        headers = reqs_reader.next()
        for row in reqs_reader:
            requirements.append(row)

    hei = []
    with codecs.open(hierarchy_path, "rb", "utf-8") as f:
        hierarchy_reader = UnicodeReader(f)
        for row in hierarchy_reader:
            hei.append(row)

    lookup = {}
    for i in range(len(groups)):
        group = groups[i]
        m = match[i]
        match_row = None
        for row in hei:
            broke = False
            if row[0] == group:
                for j in range(len(row) - 1, -1, -1):
                    if row[j] == m:
                        match_row = row
                        broke = True
                        break
                if broke:
                    break

        if match_row is not None:
            lookups = []
            for i in range(len(match_row)):
                if i == 0:
                    continue
                cell = match_row[i]
                if cell != "":
                    lookups.append(cell)

            lookup[group] = lookups

    output = ["Disposition Type", "Param"]
    idx = {}
    for i in range(len(headers)):
        h = headers[i]
        for group in groups:
            if h == group:
                idx[group] = i
                break
        for o in output:
            if "+" in o:
                o = o.split("+")
            if not isinstance(o, list):
                o = [o]
            for bit in o:
                if h == bit:
                    idx[bit] = i
                    break

    rs = []
    for r in requirements:
        score = 0
        for group in groups:
            if r[idx[group]] in lookup[group]:
                score += 1
        if score != len(groups):
            continue
        result = []
        for o in output:
            if "+" in o:
                o = o.split("+")
                text = ""
                for bit in o:
                    text += bit + " - "
                result.append(text)
            else:
                result.append(r[idx[o]])
        rs.append(result)

    sections = {}
    for r in rs:
        for i in range(len(output)):
            o = output[i]
            if o not in sections:
                sections[o] = []
            v = r[i]
            if v != "":
                sections[o].append(v)

    parts = [sections["Disposition Type"][0]] + sections["Param"]
    return "Content-Disposition: " + "; ".join(parts)

def requirements(file_cfg, config, reqs, hierarchy, groups, match, output):
    """
    reqs=tables/requirements2.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Retrieve|Empty Body|Service-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
    """
    if not isinstance(groups, list):
        groups = [groups]
    if not isinstance(match, list):
        match = [match]
    if not isinstance(output, list):
        output = [output]

    bd = config.get("src_dir")
    reqs_path = os.path.join(bd, reqs)
    hierarchy_path = os.path.join(bd, hierarchy)

    headers = []
    requirements = []
    with codecs.open(reqs_path, "rb", "utf-8") as f:
        reqs_reader = UnicodeReader(f)
        headers = reqs_reader.next()
        for row in reqs_reader:
            requirements.append(row)

    hei = []
    with codecs.open(hierarchy_path, "rb", "utf-8") as f:
        hierarchy_reader = UnicodeReader(f)
        for row in hierarchy_reader:
            hei.append(row)

    lookup = {}
    for i in range(len(groups)):
        group = groups[i]
        m = match[i]
        match_row = None
        for row in hei:
            broke = False
            if row[0] == group:
                for j in range(len(row) - 1, -1, -1):
                    if row[j] == m:
                        match_row = row
                        broke = True
                        break
                if broke:
                    break

        if match_row is not None:
            lookups = []
            for i in range(len(match_row)):
                if i == 0:
                    continue
                cell = match_row[i]
                if cell != "":
                    lookups.append(cell)

            lookup[group] = lookups

    idx = {}
    for i in range(len(headers)):
        h = headers[i]
        for group in groups:
            if h == group:
                idx[group] = i
                break
        for o in output:
            if "+" in o:
                o = o.split("+")
            if not isinstance(o, list):
                o = [o]
            for bit in o:
                if h == bit:
                    idx[bit] = i
                    break

    rs = []
    for r in requirements:
        score = 0
        for group in groups:
            if r[idx[group]] in lookup[group]:
                score += 1
        if score != len(groups):
            continue
        result = []
        for o in output:
            if "+" in o:
                o = o.split("+")
                text = ""
                for bit in o:
                    text += bit + " - "
                result.append(text)
            else:
                result.append(r[idx[o]])
        rs.append(result)

    sections = {}
    for r in rs:
        for i in range(len(output)):
            o = output[i]
            if o not in sections:
                sections[o] = []
            v = r[i]
            if v != "":
                sections[o].append(v)

    frag = ""
    for key in output:
        reqs = sections[key]
        if len(reqs) == 0:
            continue
        frag += "**" + key + "**\n\n"
        for req in reqs:
            frag += " * " + req.replace("\n", "<br>") + "\n"
        frag += "\n"
    return frag


def requirements_table(file_cf, config, source, vectors, reqs, header_level=1):
    if not isinstance(vectors, list):
        vectors = [vectors]
    if not isinstance(reqs, list):
        reqs = [reqs]
    header_level = int(header_level)

    bd = config.get("src_dir")
    path = os.path.join(bd, source)

    headers = []
    section_order = []
    sections = {}
    with codecs.open(path, "rb", "utf-8") as f:
        reader = UnicodeReader(f)
        headers = reader.next()

        idx = {}
        for i in range(len(headers)):
            h = headers[i]
            for v in vectors:
                if h == v:
                    idx[v] = i
                    break
            for r in reqs:
                if h == r:
                    idx[r] = i
                    break

        for row in reader:
            header = ""
            for v in vectors:
                if header != "":
                    header += ", "
                header += v + ": " + row[idx[v]]

            if header not in sections:
                sections[header] = {}
            if header not in section_order:
                section_order.append(header)

            for r in reqs:
                if r not in sections[header]:
                    sections[header][r] = []
                val = row[idx[r]]
                if val != "" and val not in sections[header][r]:
                    sections[header][r].append(val)

    frag = ""
    for section_header in section_order:
        requirements = sections[section_header]
        section_header = section_header.replace("*", "\*")

        frag += "#" * header_level + " " + section_header + "\n\n"

        for req_title in reqs:
            req_list = requirements[req_title]
            if len(req_list) == 0:
                continue
            frag += "**" + req_title + "**\n\n"
            for req_entry in req_list:
                text = markdown.markdown(req_entry)[3:-4]
                text = text.replace("\n", "")
                frag += " * " + text + "\n"
            frag += "\n"

    return frag

def requirements_table_2(file_cf, config, source, vectors, reqs, definitions=None, header_level=1):
    if not isinstance(vectors, list):
        vectors = [vectors]
    if not isinstance(reqs, list):
        reqs = [reqs]
    header_level = int(header_level)

    bd = config.get("src_dir")
    path = os.path.join(bd, source)

    defs = {}
    if definitions is not None:
        def_src = os.path.join(bd, definitions)
        with codecs.open(def_src, "rb", "utf-8") as f:
            reader = UnicodeReader(f)
            headers = reader.next()
            defs = {headers[0] : {}}
            for row in reader:
                defs[headers[0]][row[0]] = row[1]

    headers = []
    section_order = []
    sections = {}
    with codecs.open(path, "rb", "utf-8") as f:
        reader = UnicodeReader(f)
        headers = reader.next()

        idx = {}
        for i in range(len(headers)):
            h = headers[i]
            for v in vectors:
                if h == v:
                    idx[v] = i
                    break
            for r in reqs:
                if h == r:
                    idx[r] = i
                    break

        vector_sections = []
        expanded_requirements = {}
        for row in reader:
            vector_section = []
            for v in vectors:
                vector_section.append(row[idx[v]])
            if not vector_section in vector_sections:
                vector_sections.append(vector_section)
            id = vector_sections.index(vector_section)
            if id not in expanded_requirements:
                expanded_requirements[id] = {}
            for r in reqs:
                if r not in expanded_requirements[id]:
                    expanded_requirements[id][r] = []
                val = row[idx[r]]
                if val != "" and val not in expanded_requirements[id][r]:
                    expanded_requirements[id][r].append(val)

        total_width = len(vectors) * len(reqs)
        vector_width = len(reqs)
        req_width = len(vectors)

        frag = '<table><thead><tr>'
        for v in vectors:
            frag += '<td colspan="' + str(vector_width) + '" style="text-align: center"><strong>' + v + '</strong></td>'
        frag += "</tr></thead>"

        for i in range(len(vector_sections)):
            vs = vector_sections[i]
            frag += '<tr>'
            for vname in vs:
                frag += '<td colspan="' + str(vector_width) + '" style="text-align: center">' + vname + "</td>"
            frag += "</tr><tr>"
            for r in reqs:
                frag += '<td colspan="' + str(req_width) + '"><strong>' + r + "</strong></td>"
            frag += "</tr><tr>"
            context = expanded_requirements[i]
            for r in reqs:
                vals = context[r]
                cell = ""
                for v in vals:
                    deftext = ""
                    if r in defs:
                        deftext = " - " + defs[r][v]
                    cell += " * " + v + deftext + "\n"
                    cell = markdown.markdown(cell)
                frag += '<td colspan="' + str(req_width) + '">' + cell + '</td>'
            frag += "</tr>"
        frag += "</table>"

    return frag


def requirements_hierarchy(file_cfg, config, source, key):
    bd = config.get("src_dir")
    path = os.path.join(bd, source)

    rows = []
    with codecs.open(path, "rb", "utf-8") as f:
        reader = UnicodeReader(f)
        for row in reader:
            if row[0] == key:
                rows.append(row[1:])

    h = {}
    context = h
    for row in rows:
        for cell in row:
            if cell == "":
                break
            if cell not in context:
                context[cell] = {}
            context = context[cell]
        context = h

    def _recurse_heirarchy(node, depth):
        frag = ""
        for k, v in node.iteritems():
            frag += "\t" * (depth - 1) + "* " + k.replace("*", "\*") + "\n"
            if len(v.keys()) != 0:
                frag += _recurse_heirarchy(v, depth + 1)
        return frag

    frag = _recurse_heirarchy(h, 1)
    return frag


def overlay_requirements(file_cfg, config, source, groups=None, order=None):
    if not isinstance(groups, list):
        groups = [groups]
    bd = config.get("src_dir")
    path = os.path.join(bd, source)
    with codecs.open(path, "rb", "utf-8") as f:
        reader = UnicodeReader(f)
        headers = reader.next()
        requirements = {}
        group_name = None
        for row in reader:
            if row[0].startswith("Group: "):
                group_name = row[0][len("Group: "):]
                requirements[group_name] = {}
                for header in headers:
                    requirements[group_name][header] = []
            else:
                if group_name not in groups:
                    continue
                for i in range(len(row)):
                    cell = row[i]
                    header = headers[i]
                    if cell != "" and cell not in requirements[group_name][header]:
                        requirements[group_name][header].append(cell)

    sections = {}
    for group in groups:
        reqs = requirements[group]
        for header in headers:
            if header not in sections:
                sections[header] = []
            sections[header] += reqs[header]

    if order is None:
        order = headers

    frag = ""
    for key in order:
        reqs = sections[key]
        if len(reqs) == 0:
            continue
        frag += "**" + key + "**\n\n"
        for req in reqs:
            frag += " * " + req.replace("\n", "<br>") + "\n"
        frag += "\n"
    return frag


def define(file_cfg, config, resource, id):
    rpath = config.get("resources", {}).get(resource)
    with codecs.open(rpath, "rb", "utf-8") as f:
        reader = UnicodeReader(f)
        headers = reader.next()
        for row in reader:
            if row[0] == id:
                return id + '<sup>[<a href="#' + _anchor_name(id) + '">def</a>]</sup>'
    raise BuildException("Unable to find definition for " + id)

def link(file_cfg, config, header):
    toc = file_cfg["toc"]
    for k, v in toc.iteritems():
        if v == header:
            return "[" + header + "](#" + k + ")"
    raise BuildException("Unable to find header " + header)

def toc(file_cfg, config):
    contents = file_cfg["toc"]
    numbers = contents.keys()
    numbers.sort(key=lambda s: [int(u) for u in s.split('.') if u != ""])
    frag = "{~ html div,clazz=toc ~}\n\n"
    for n in numbers:
        indent = len(n.split(".")) - 2
        frag += "\t" * indent + "* [" + n + " " + contents[n] + "](#" + n + ")\n"
    frag += "{~ html /div ~}\n\n"
    return frag

def json_schema_definitions(file_cfg, config, schema_file):
    bd = config.get("src_dir")
    path = os.path.join(bd, schema_file)
    with codecs.open(path, "rb", "utf-8") as f:
        js = json.loads(f.read())
    rows = []

    def _recurse_properties(rows, props, prefix):
        for prop, val in props.iteritems():
            title = val.get("title", "")
            desc = val.get("description", "")
            text = ""
            if title != "":
                text = title
            if desc != "":
                if text != "":
                    text += "\n\n"
                text += desc
            field_name = prefix + prop
            rows.append([field_name, val.get("type"), text])

            if "properties" in val:
                _recurse_properties(rows, val.get("properties", {}), field_name + ".")
            elif "items" in val:
                if "properties" in val.get("items", {}):
                    _recurse_properties(rows, val.get("items", {}).get("properties", {}), field_name + "[].")

    _recurse_properties(rows, js.get("properties", {}), "")
    _recurse_properties(rows, js.get("patternProperties", {}), "")

    rows.sort(key=lambda x: x[0])
    frag =  "| Field | Type | Description |\n"
    frag += "| ----- | ---- | ----------- |\n"
    for row in rows:
        desc = row[2]
        desc = desc.replace("\n", "<br>")
        frag += "| " + row[0] + " | " + row[1] + " | " + desc + " |\n"
    return frag


def _anchor_name(v):
    v = v.lower().strip()
    return v.replace(" ", "_")


def html(file_cfg, config, element, clazz=None):
    if clazz is not None and not isinstance(clazz, list):
        clazz = [clazz]

    tag = "<" + element
    if clazz is not None:
        tag += " class=" + " ".join(clazz)
    tag += ">"

    return tag

def json_extract(file_cfg, config, source, keys=None, selector=None):
    if keys is not None and not isinstance(keys, list):
        keys = [keys]

    bd = config.get("src_dir")
    path = os.path.join(bd, source)
    with codecs.open(path, "rb", "utf-8") as f:
        js = json.loads(f.read())

    if selector is not None:
        js = js[selector]

    show = {}
    if keys is None:
        show = js
    else:
        for key in keys:
            if key in js:
                show[key] = js[key]

    out = json.dumps(show, indent=2)
    return out

def sections(file_cfg, config, source, header_field, header_level, order, list_fields, intro):
    if not isinstance(order, list):
        order = [order]
    if not isinstance(list_fields, list):
        list_fields = [list_fields]
    if not isinstance(intro, list):
        intro = [intro]
    header_level = int(header_level)

    intros = {}
    for pair in intro:
        bits = pair.split(":")
        intros[bits[0]] = bits[1]

    bd = config.get("src_dir")
    path = os.path.join(bd, source)
    with codecs.open(path, "rb", "utf-8") as f:
        reader = UnicodeReader(f)
        headers = reader.next()

        hindex = 0
        for i in range(len(headers)):
            h = headers[i]
            if header_field == h:
                hindex = i

        oindex = []
        for o in order:
            for i in range(len(headers)):
                if o == headers[i]:
                    oindex.append(i)
                    break

        frag = ""
        for row in reader:
            frag += "#" * header_level + " " + row[hindex] + "\n\n"
            for o in oindex:
                content = row[o]
                if content == "":
                    continue
                if headers[o] in intros:
                    frag += intros[headers[o]] + "\n\n"
                if headers[o] in list_fields:
                    thelist = ""
                    bits = [c.strip() for c in content.split(",")]
                    for b in bits:
                        thelist += " * " + b + "\n"
                    content = thelist
                frag += content + "\n\n"

        return frag

def img(file_cfg, config, target, alt=None):
    base = config.get("base_url")
    altText = ""
    if alt is not None:
        altText = alt
    frag = '<div><img src="' + base + target + '" alt="' + altText + '"></div>'
    return frag

def fig(file_cfg, config, target, alt=None):
    frag = img(file_cfg, config, target, alt)
    if alt is not None:
        if "figures" not in file_cfg:
            file_cfg["figures"] = []
        altText = "Figure " + str(len(file_cfg["figures"]) + 1) + ": " + alt
        frag += '<div class="figure_label">' + altText + '</div>'
        file_cfg["figures"].append(alt)
    return frag

def title_slide(file_cfg, config, title, subtitle="", attribution=""):
    frag = "<h2>" + title + "</h2>"
    if subtitle != "":
        frag += "<h3>" + subtitle + "</h3>"
    frag += "\n\n"
    frag += attribution
    return frag

############

COMMANDS = {
    "include" : include,
    "ref" : ref,
    "date" : date,
    "table_rows_as_paras" : table_rows_as_paras,
    "dl" : dl,
    "table" : table,
    "openapi_list_descriptions" : openapi_list_descriptions,
    "url" : url,
    "openapi_paths" : openapi_paths,
    "aggregated_requirements" : aggregated_requirements,
    "def" : define,
    "overlay_requirements" : overlay_requirements,
    "link" : link,
    "toc" : toc,
    "json_schema_definitions" : json_schema_definitions,
    "requirements" : requirements,
    "requirements_table" : requirements_table,
    "requirements_table_2" : requirements_table_2,
    "requirements_hierarchy" : requirements_hierarchy,
    "html" : html,
    "json_extract" : json_extract,
    "sections" : sections,
    "img" : img,
    "fig" : fig,
    "content_disposition" : content_disposition,
    "title_slide" : title_slide,
    "http_exchange" : http_exchange
}

EXPAND_COMMANDS = ["include", "openapi_paths", "requirements_table"]

POST_RENDER = ["html"]

##################################################

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config file for build")
    parser.add_argument("-m", "--mode", help="the build mode for this file 'live' or 'dev'")
    args = parser.parse_args()

    config = None
    with codecs.open(args.config) as f:
        config = json.loads(f.read())

    if args.mode == "live":
        config["base_url"] = config["base_urls"]["live"]
    elif args.mode == "dev":
        config["base_url"] = config["base_urls"]["dev"]

    run(config)