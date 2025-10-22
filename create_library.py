import sys
import zlib
import base64
import os, os.path, sys
import glob
from xml.etree import ElementTree

def decode_base64_and_inflate( b64string ):
    decoded_data = base64.b64decode( b64string )
    return zlib.decompress( decoded_data , -15)

def deflate_and_base64_encode( string_val ):
    zlibbed_str = zlib.compress( string_val )
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode( compressed_string )

def save_library( FileName, LibraryString):
    FileName += f'''.drawio'''
    text_file = open(FileName, "w")
    text_file.write(LibraryString)
    text_file.close()

def Append_Library_End (LibraryString):
    LibraryString = LibraryString[:-1]
    LibraryString += f''']</mxlibrary>'''
    return LibraryString

def Append_Library (FileName):
    file_path = FileName
    with open(file_path, 'r') as file:
        file_content = file.read()

    file_content = file_content[:-14]
    file_content += ','
    
    return file_content[12:]

def Generate_Library_String_One_Row(StartNum, StopNum):
    """Optional docstring: describes what the function does."""
    output = f''''''
    for nnn in range(StartNum, StopNum):
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

        encodedstring = deflate_and_base64_encode(fullstring.encode('utf-8'))
        shape_stencil = encodedstring.decode("utf-8")
        output += f'''
        {{
            "xml": "&lt;mxGraphModel&gt;&lt;root&gt;&lt;mxCell id=\\"0\\"/&gt;&lt;mxCell id=\\"1\\" parent=\\"0\\"/&gt;&lt;mxCell id=\\"2\\" value=\\"\\" style=\\"shape=stencil({shape_stencil});whiteSpace=wrap;html=1;\\" vertex=\\"1\\" parent=\\"1\\"&gt;&lt;mxGeometry width=\\"{shapeW}\\" height=\\"{shapeH}\\" as=\\"geometry\\"/&gt;&lt;/mxCell&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;",
            "w": {shapeW},
            "h": {shapeH}
        }},'''

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

    return output  # optional

def Generate_Library_String_Double_Row(doublerow_pincount):
    """Optional docstring: describes what the function does."""
    output = f''''''
    for nnn in doublerow_pincount:
        factor = 2
        nRows = 2
        nCons = nnn
        shapeH= (nCons/nRows+1)* factor * 10
        shapeW= 40 * factor

        #NORMAL
        fullstring = "<shape h=\"" + str(shapeH) + "\" w=\"" + str(shapeW) + "\" aspect=\"fixed\" strokewidth=\"inherit\">\n"
        fullstring += "  <connections>\n"
        for x in range (1,nCons+1):
            if x % 2 == 1:
                fullstring += "    <constraint x=\"0\" y=\"" + str(round((x/2+0.5) * (1/(nCons/nRows+1)),4)) + "\" perimeter=\"0\" />\n"
            else:
                fullstring += "    <constraint x=\"1\" y=\"" + str(round((x/2) * (1/(nCons/nRows+1)),4)) + "\" perimeter=\"0\" />\n"
        fullstring += "  </connections>\n"
        fullstring += "  <background>\n"
        fullstring += "    <rect x=\"0\" y=\"0\" h=\"" + str(shapeH) + "\" w=\"" + str(shapeW) + "\" />\n"
        fullstring += "  </background>\n"
        fullstring += "  <foreground>\n"
        fullstring += "    <fillstroke />\n"
        for x in range (1,nCons+1):
            fullstring += "    <path>\n"
            if x % 2 == 1:
                fullstring += "      <move x=\"0\" y=\"" + str(x*10*factor/nRows+10*(factor-1)) + "\" />\n"
                fullstring += "      <line x=\"-10\" y=\"" + str(x*10*factor/nRows+10*(factor-1)) + "\" />\n"
            else:
                fullstring += "      <move x=\"80\" y=\"" + str((x-1)*10*factor/nRows+10*(factor-1)) + "\" />\n"
                fullstring += "      <line x=\"90\" y=\"" + str((x-1)*10*factor/nRows+10*(factor-1)) + "\" />\n"            
            fullstring += "    </path>\n"
            fullstring += "    <stroke />\n"
            if x % 2 == 1:
                fullstring += "    <text str=\"" + str(x) + "\" x=\"10\" y=\"" + str(x*10*factor/nRows+10*(factor-1)) + "\" align = \"center\" valign=\"middle\" align-shape=\"0\"/>"
            else:
                fullstring += "    <text str=\"" + str(x) + "\" x=\"70\" y=\"" + str((x-1)*10*factor/nRows+10*(factor-1)) + "\" align = \"center\" valign=\"middle\" align-shape=\"0\"/>"
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

    return output # optional


#### 1-100 Connectors ####
output1 = f'''<mxlibrary>['''
SingleConnectorString = Generate_Library_String_One_Row(1, 100)
output1 += SingleConnectorString
output1 = Append_Library_End(output1)
save_library('QS_ARCH_TEMPLATE__CONNECTORS_SINGLE_ROW', output1)


#### DoubleRow #####
output2 = f'''<mxlibrary>['''
DoubleConnectorString = Generate_Library_String_Double_Row([20, 60, 120])
output2 += DoubleConnectorString
output2 = Append_Library_End(output2)
save_library('QS_ARCH_TEMPLATE__CONNECTORS_DOUBLE_ROW', output2)

#### Combined Library #####
output3 = f'''<mxlibrary>['''
output3 += SingleConnectorString
output3 += DoubleConnectorString
output3 += Append_Library('QS_ARCH_TEMPLATE__BUSSES.drawio')
output3 += Append_Library('QS_ARCH_TEMPLATE__SYSTEMS.drawio')
output3 = Append_Library_End(output3)
save_library('QS_ARCH_TEMPLATE__COMBINED', output3)



