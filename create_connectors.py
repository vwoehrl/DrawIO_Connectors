import sys
import zlib
import base64

def decode_base64_and_inflate( b64string ):
    decoded_data = base64.b64decode( b64string )
    return zlib.decompress( decoded_data , -15)

def deflate_and_base64_encode( string_val ):
    zlibbed_str = zlib.compress( string_val )
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode( compressed_string )

output = f'''<mxlibrary>['''

for nnn in range(1, 60):
    factor = 2
    nCons = nnn
    shapeH= (nCons+1)* factor * 10
    shapeW= 40 * factor
    reverse = True

    #NORMAL
    fullstring = "<shape h=\"" + str(shapeH) + "\" w=\"" + str(shapeW) + "\" aspect=\"fixed\" strokewidth=\"inherit\">\n"
    fullstring += "  <connections>\n"
    for x in range (1,nCons+1):
        fullstring += "    <constraint x=\"0\" y=\"" + str(round(x * (1/(nCons+1)),4)) + "\" perimeter=\"0\" />\n"
    fullstring += "  </connections>\n"
    fullstring += "  <background>\n"
    fullstring += "    <rect x=\"0\" y=\"0\" h=\"" + str(shapeH) + "\" w=\"" + str(shapeW) + "\" />\n"
    fullstring += "  </background>\n"
    fullstring += "  <foreground>\n"
    fullstring += "    <fillstroke />\n"
    for x in range (1,nCons+1):
        fullstring += "    <path>\n"
        fullstring += "      <move x=\"0\" y=\"" + str(x*10*factor) + "\" />\n"
        fullstring += "      <line x=\"-10\" y=\"" + str(x*10*factor) + "\" />\n"
        fullstring += "    </path>\n"
        fullstring += "    <stroke />\n"
        fullstring += "    <text str=\"" + str(x) + "\" x=\"10\" y=\"" + str(x*10*factor) + "\" align = \"center\" valign=\"middle\" align-shape=\"0\"/>"
        fullstring += "    <stroke />"
    fullstring += "  </foreground>\n"
    fullstring += "</shape>\n"
    #print(fullstring)

    encodedstring = deflate_and_base64_encode(fullstring.encode('utf-8'))
    shape_stencil = encodedstring.decode("utf-8")
    output += f'''
    {{
        "xml": "&lt;mxGraphModel&gt;&lt;root&gt;&lt;mxCell id=\\"0\\"/&gt;&lt;mxCell id=\\"1\\" parent=\\"0\\"/&gt;&lt;mxCell id=\\"2\\" value=\\"\\" style=\\"shape=stencil({shape_stencil});whiteSpace=wrap;html=1;\\" vertex=\\"1\\" parent=\\"1\\"&gt;&lt;mxGeometry width=\\"{shapeW}\\" height=\\"{shapeH}\\" as=\\"geometry\\"/&gt;&lt;/mxCell&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;",
        "w": {shapeW},
        "h": {shapeH}
    }},'''

    # Generate Shape XML Normal
    # filestring = str(nCons) + "P_CON.xml"
    # text_file = open(filestring, "w")
    # text_file.write(fullstring)
    # text_file.close()

    #REVERSE
    fullstringR = "<shape h=\"" + str(shapeH) + "\" w=\"" + str(shapeW) + "\" aspect=\"fixed\" strokewidth=\"inherit\">\n"
    fullstringR += "  <connections>\n"
    for x in range (1,nCons+1):
        fullstringR += "    <constraint x=\"0\" y=\"" + str(round(x * (1/(nCons+1)),4)) + "\" perimeter=\"0\" />\n"
    fullstringR += "  </connections>\n"
    fullstringR += "  <background>\n"
    fullstringR += "    <rect x=\"0\" y=\"0\" h=\"" + str(shapeH) + "\" w=\"" + str(shapeW) + "\" />\n"
    fullstringR += "  </background>\n"
    fullstringR += "  <foreground>\n"
    fullstringR += "    <fillstroke />\n"
    for x in range (1,nCons+1):
        fullstringR += "    <path>\n"
        fullstringR += "      <move x=\"0\" y=\"" + str(x*10*factor) + "\" />\n"
        fullstringR += "      <line x=\"-10\" y=\"" + str(x*10*factor) + "\" />\n"
        fullstringR += "    </path>\n"
        fullstringR += "    <stroke />\n"
        fullstringR += "    <text str=\"" + str(nCons+1-x) + "\" x=\"10\" y=\"" + str(x*10*factor) + "\" align = \"center\" valign=\"middle\" align-shape=\"0\"/>"
        fullstringR += "    <stroke />"
    fullstringR += "  </foreground>\n"
    fullstringR += "</shape>\n"
    #print(fullstringR)

    encodedstring = deflate_and_base64_encode(fullstringR.encode('utf-8'))
    shape_stencilR = encodedstring.decode("utf-8")
    output += f'''
    {{
        "xml": "&lt;mxGraphModel&gt;&lt;root&gt;&lt;mxCell id=\\"0\\"/&gt;&lt;mxCell id=\\"1\\" parent=\\"0\\"/&gt;&lt;mxCell id=\\"2\\" value=\\"\\" style=\\"shape=stencil({shape_stencilR});whiteSpace=wrap;html=1;\\" vertex=\\"1\\" parent=\\"1\\"&gt;&lt;mxGeometry width=\\"{shapeW}\\" height=\\"{shapeH}\\" as=\\"geometry\\"/&gt;&lt;/mxCell&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;",
        "w": {shapeW},
        "h": {shapeH}
    }},'''

    # Generate Shape XML Reverse
    # filestring = str(nCons) + "P_CON_Reverse.xml"
    # text_file = open(filestring, "w")
    # text_file.write(fullstringR)
    # text_file.close()


# WRITE LIBRARY
output = output[:-1]
output += f'''
]</mxlibrary>'''
# print(output)

filestringLib = "Connectors.drawio"
text_file = open(filestringLib, "w")
text_file.write(output)
text_file.close()