import xml.etree.ElementTree as ET
import os
import re

class JavaGenerator:
    def __init__(self, xml_string):
        cleaned_xml = xml_string.replace('\xa0', ' ').strip()
        try:
            self.root = ET.fromstring(cleaned_xml)
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            exit(1)
            
        self.entities = {} 
        self.edges = []    
        self.classes = {}

    def parse(self):
        for cell in self.root.findall(".//mxCell"):
            value = cell.get('value', '')
            if cell.get('vertex') == '1' and value:
                clean_name = re.sub('<[^<]+?>', '', value).strip()
                if " " not in clean_name or clean_name in ["Menu Item"]:
                    cid = cell.get('id')
                    name = clean_name.replace(" ", "")
                    self.entities[cid] = name
                    self.classes[name] = {'attrs': [], 'parent': None}

        for cell in self.root.findall(".//mxCell"):
            if cell.get('edge') == '1':
                source = cell.get('source')
                target = cell.get('target')
                value = cell.get('value', '')
                clean_val = re.sub('<[^<]+?>', '', value).strip().lower()
                self.edges.append((source, target, clean_val))

        for src_id, tgt_id, desc in self.edges:
            if src_id in self.entities and tgt_id in self.entities:
                src_name = self.entities[src_id]
                tgt_name = self.entities[tgt_id]

                if tgt_name == "Person" and not desc:
                    self.classes[src_name]['parent'] = "Person"
                elif desc:
                    is_many = "n" in desc or "*" in desc
                    attr_type = f"List<{tgt_name}>" if is_many else tgt_name
                    attr_name = tgt_name.lower() + ("s" if is_many else "")
                    self.classes[src_name]['attrs'].append((attr_type, attr_name))
                else:
                    self.classes[src_name]['attrs'].append((tgt_name, tgt_name.lower()))

    def generate_java(self, output_dir="src-gen"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for name, data in self.classes.items():
            is_abstract = "abstract " if name == "Person" else ""
            extends = f" extends {data['parent']}" if data['parent'] else ""
            
            lines = [
                "import java.util.*;",
                "",
                f"public {is_abstract}class {name}{extends} {{"
            ]

            if name == "Person":
                lines.append("    private String name;")
                lines.append("    private String phoneNumber;")

            for dtype, dname in data['attrs']:
                lines.append(f"    private {dtype} {dname};")

            lines.append("")
            lines.append(f"    public {name}() {{}}")
            lines.append("")

            for dtype, dname in data['attrs']:
                method_name = dname[0].upper() + dname[1:]
                lines.append(f"    public {dtype} get{method_name}() {{")
                lines.append(f"        return this.{dname};")
                lines.append("    }")
                lines.append("")

            lines.append("}")
            
            with open(os.path.join(output_dir, f"{name}.java"), "w") as f:
                f.write("\n".join(lines))
        
        print(f"Successfully generated {len(self.classes)} Java files in ./{output_dir}")

xml_data = """<mxGraphModel dx="1042" dy="535" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <mxCell id="dBT3p7U1jRL56inFbdlT-1" value="Person" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
      <mxGeometry x="310" y="90" width="160" height="60" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-5" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=1;entryDx=0;entryDy=0;" edge="1" parent="1" source="dBT3p7U1jRL56inFbdlT-2" target="dBT3p7U1jRL56inFbdlT-1">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="230" y="180" />
          <mxPoint x="390" y="180" />
        </Array>
      </mxGeometry>
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-10" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="dBT3p7U1jRL56inFbdlT-2" target="dBT3p7U1jRL56inFbdlT-8">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-2" value="Customer" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
      <mxGeometry x="170" y="190" width="120" height="60" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-7" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="dBT3p7U1jRL56inFbdlT-3" target="dBT3p7U1jRL56inFbdlT-1">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="550" y="180" />
          <mxPoint x="390" y="180" />
        </Array>
      </mxGeometry>
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-11" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="dBT3p7U1jRL56inFbdlT-3" target="dBT3p7U1jRL56inFbdlT-9">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-3" value="Courier" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
      <mxGeometry x="490" y="190" width="120" height="60" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-12" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="dBT3p7U1jRL56inFbdlT-8" target="dBT3p7U1jRL56inFbdlT-9">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-18" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="dBT3p7U1jRL56inFbdlT-8" target="dBT3p7U1jRL56inFbdlT-15">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-8" value="Order" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
      <mxGeometry x="170" y="310" width="120" height="60" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-17" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="dBT3p7U1jRL56inFbdlT-9" target="dBT3p7U1jRL56inFbdlT-16">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-9" value="Delivery" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
      <mxGeometry x="490" y="310" width="120" height="60" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-13" value="Creates 1" style="text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
      <mxGeometry x="360" y="300" width="60" height="30" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-14" value="Places N" style="text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
      <mxGeometry x="240" y="260" width="60" height="30" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-15" value="Menu Item" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
      <mxGeometry x="170" y="420" width="120" height="60" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-16" value="Address" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
      <mxGeometry x="490" y="420" width="120" height="60" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-20" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=1;entryDx=0;entryDy=0;" edge="1" parent="1" source="dBT3p7U1jRL56inFbdlT-19" target="dBT3p7U1jRL56inFbdlT-15">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-19" value="Menu" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
      <mxGeometry x="170" y="530" width="120" height="60" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-21" value="Contains N" style="text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
      <mxGeometry x="250" y="490" width="70" height="30" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-22" value="Includes N" style="text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
      <mxGeometry x="240" y="380" width="60" height="30" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-23" value="Delivered to 1 " style="text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
      <mxGeometry x="570" y="380" width="80" height="30" as="geometry" />
    </mxCell>
    <mxCell id="dBT3p7U1jRL56inFbdlT-25" value="Fulfills N" style="text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
      <mxGeometry x="570" y="260" width="60" height="30" as="geometry" />
    </mxCell>
  </root>
</mxGraphModel>"""

if __name__ == "__main__":
    gen = JavaGenerator(xml_data)
    gen.parse()
    gen.generate_java()