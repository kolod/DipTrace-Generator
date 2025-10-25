# DipTrace Pattern Library XML File format specification

With the default value, some parameters are not written to the file.

## 1. File title

```xml
<?xml version="1.0" encoding="UTF-8"?>
```

Description of the XML file version and encoding.

## 2. Information about library file, \<Library\>

```xml
<Library Type="DipTrace-PatternLibrary" Name="BGA Pitch 0.35mm" Hint="Ball Grid Array -
Pitch 0.35mm" Version="4.3.0.1" Units="inch">
```

| Name     | Type  | Description                                                                                     |
|:--------:|:-----:|:------------------------------------------------------------------------------------------------|
| Type     | Text  | "DipTrace-PatternLibrary" – file created in DipTrace Pattern Editor for PCB footprints.         |
| Name     | Text  | Library name on the Library panel.                                                              |
| Hint     | Text  | Library hint text on the Library panel.                                                         |
| Version  | Text  | Version of the library file format.                                                             |
| Units    | Text  | Measurement units of dimensions in the file: "mm" – millimetres; "inch" – inches; "mil" – mils. |

## 3. Pad Style description section, \<PadStyles\>

```xml
<PadStyles>  – start of the pad style description section.
{...}        – pad style description (PadStyle).
</PadStyles> – end of the pad style description section.
```

## 3.1. Pad Style description, \<PadStyle\>

```xml
<PadStyle Name="PadT3" Type="Through" HoleType="Round" Hole="0.0354" Side="Top">
    <MainStack Shape="Obround" Width="0.0591" Height="0.0591" XOff="0" Off="0" />
</PadStyle>
```

| Name     | Type  | Description                                                                               |
|:--------:|:-----:|:------------------------------------------------------------------------------------------|
| Name     | Text  | Pad style name.                                                                           |
| Type     | Text  | Pad type: "surface" – surface pad; "through" – through pad.                               |
| HoleType | Text  | Hole shape: "Round" – round; "Obround" – obround.                                         |
| Hole     | Real  | Hole Real Diameter for Round Hole, width for Obround Hole. Keepout diameter for Fiducial. |
| HoleH    | Real  | Obround hole height.                                                                      |
| Side     | Text  | Pad location side: "Top" – pad on the Top side; "Bottom" – pad on the Bottom side.        |

## 3.1.1. Main pad shape parameters, \<MainStack\>

```xml
<MainStack Shape="Polygon" Width="1" Height="0.6" XOff="0" YOff="0">
```

| Name     | Type  | Description                                                                               |
|:--------:|:-----:|:------------------------------------------------------------------------------------------|
| Shape    | Text  | Pad shape: "Ellipse"; "Obround"; "Rectangle"; "Polygon"; "D-shape"; "Fiducial".           |
| Width    | Real  | Pad width. Copper diameter for Fiducial.                                                  |
| Height   | Real  | Pad height.                                                                               |
| XOff     | Real  | X offset of the shape of a through pad relative to its center (hole).                     |
| YOff     | Real  | Y offset of the shape of a through pad relative to its center (hole).                     |
| Corner   | Real  | Rounding of the corners of a rectangular pad as a percentage of the shorter side: 0 - for Rectangle, 0..50 - for Roundrect. |

## 3.1.1.1. List of polygonal pad points, \<Points\>

```xml
<Points>  – start of the list of polygonal pad points;
{...}     – list of coordinates of the points (Item);
</Points> – end of the list of polygonal pad points.
```

## 3.1.1.1.1 Coordinates of points of polygonal pad relative to its center, \<Item\>

```xml
<Item X="0.5" Y="0.2"/>
```

| Name     | Type  | Description                                                                               |
|:--------:|:-----:|:------------------------------------------------------------------------------------------|
| X       | Real  | X coordinate.                                                                              |
| Y       | Real  | Y coordinate.                                                                              |

## 3.1.2. List of the shapes of Terminals, \<Terminals\>

```xml
<Terminals>  – start of the list of Terminals;
{...}        – list of the shapes of Terminals (Terminal, max. 4 shapes);
</Terminals> – end of the list of Terminals.
```

## 3.1.2.1. Terminal shape description, \<Terminal\>

```xml
<Terminal Shape="Rectangle" X="0" Y="0" Angle="0" Width="0.8" Height="0.4" Corner="0"/>
```

| Name     | Type  | Description                                                                               |
|:--------:|:-----:|:------------------------------------------------------------------------------------------|
| Shape    | Text  | Terminal shape type: "Obround"; "Rectangle"; "Polygon"; "D-shape".                        |
| X        | Real  | X offset – terminal shape position on the pad (center of the shape).                      |
| Y        | Real  | Y offset – terminal shape position on the pad (center of the shape).                      |
| Angle    | Real  | Angle of the terminal shape in radians, counterclockwise.                                 |
| Width    | Real  | Shape Width.                                                                              |
| Height   | Real  | Shape Height.                                                                             |
| Corner   | Real  | Shape Corner radius as percentage of the shorter side: 0 - for Rectangle, 0..50 – for Roundrect. |

## 3.1.2.1.1. List of points of polygonal Terminal, \<Points\>

```xml
<Points>  – start of the list of polygonal terminal points;
{...}     – list of coordinates of points (Item);
</Points> – end of the list of polygonal terminal points.
```

## 3.1.2.1.1.1. Coordinates of points of polygonal terminal relative to its center, \<Item\>

```xml
<Item X="0.2" Y="0.1"/>
```

| Name     | Type  | Description                                                                               |
|:--------:|:-----:|:------------------------------------------------------------------------------------------|
| X        | Real  | X coordinate.                                                                             |
| Y        | Real  | Y coordinate.                                                                             |


## 3.1.3. Pad Mask and Paste settings, \<MaskPaste\>

```xml
<MaskPaste TopMask="Tented" BotMask="Open" TopPaste="Solder" BotPaste="Segments"
Segment_Percent="50" Segment_EdgeGap="0.3" Segment_Gap="0.2" Segment_Side="1"
CustomSwell="0.12" CustomShrink="0.11">
    <BotSegments>
        <Item X1="-1.43" Y1="0.707" X2="-0.37" Y2="-0.707"/>
        <Item X1="0.37" Y1="0.707" X2="1.43" Y2="-0.707"/>
    </BotSegments>
</MaskPaste>
```

| Name            | Type  | Description                                                                        |
|:---------------:|:-----:|:-----------------------------------------------------------------------------------|
| TopMask         | Text  | TopMask Text Mask in Top layer: "Common", "Open", "Tented", "By Paste".            |
| BotMask         | Text  | Bottom Mask in Bottom layer: "Common", "Open", "Tented", "By Paste".               |
| TopPaste        | Text  | TopPaste Text Paste in Top layer: "Common", "Solder", "No Solder", "Segments".     |
| BotPaste        | Text  | Bottom Paste in Bottom layer: "Common", "Solder", "No Solder", "Segments".         |
| Segment_Percent | Real  | Fill percent for segmented paste mask.                                             |
| Segment_EdgeGap | Real  | Minimum edge clearance for segmented paste mask.                                   |
| Segment_Gap     | Real  | Minimum clearance between segments for segmented paste mask.                       |
| Segment_Side    | Real  | Minimum segment side for segmented paste mask.                                     |
| CustomSwell     | Real  | Solder Mask Swell.                                                                 |
| CustomShrink    | Real  | Paste Mask Shrink.                                                                 |

## 3.1.3.1. List of paste segments in Top layer for segmented paste, \<TopSegments\>

```xml
<TopSegments>  – start of the list of segments;
{...}          – list of segments (Item);
</TopSegments> – end of the list of segments.
```

## 3.1.3.1.1. Diagonal coordinates of the paste segments in the Top layer for segmented paste, \<Item\>

| Name     | Type  | Description                                                                               |
|:--------:|:-----:|:------------------------------------------------------------------------------------------|
| X1       | Real  | X coordinate of the first diagonal point.                                                 |
| Y1       | Real  | Y coordinate of the first diagonal point.                                                 |
| X2       | Real  | X coordinate of the second diagonal point.                                                |
| Y2       | Real  | Y coordinate of the second diagonal point.                                                |

```plaintext
            ┌─────────── • (X2, Y2)
            │            │
            │            │
            │            │
   (X1, Y1) • ───────────┘ 
```

(X1, Y1) – coordinates of the first diagonal point at bottom left.  
(X2, Y2) – coordinates of the second diagonal point at top right.

## 3.1.3.2. List of paste segments in Bottom layer for segmented paste, \<BotSegments\>

```xml
<BotSegments>  – start of the list of segments;
{...}          – list of segments (Item);
</BotSegments> – end of the list of segments.
```

## 3.1.3.2.1. Diagonal coordinates of the paste segments in the Bottom layer for segmented paste, \<Item\>

| Name     | Type  | Description                                                                               |
|:--------:|:-----:|:------------------------------------------------------------------------------------------|
| X1       | Real  | X coordinate of the first diagonal point.                                                 |
| Y1       | Real  | Y coordinate of the first diagonal point.                                                 |
| X2       | Real  | X coordinate of the second diagonal point.                                                |
| Y2       | Real  | Y coordinate of the second diagonal point.                                                |

```plaintext
            ┌─────────── • (X2, Y2)
            │            │
            │            │
            │            │
   (X1, Y1) • ───────────┘
```

(X1, Y1) – coordinates of the first diagonal point at bottom left.  
(X2, Y2) – coordinates of the second diagonal point at top right.

## 4. Description of Pattern Categories used, \<Categories\>

```xml
<Categories>  – start of the list of categories;
{...}         – list of categories (Category);
</Categories> – end of the list of categories.
```

## 4.1. Category description, \<Category\>

## 4.1.1. Category number

```xml
<Category Number="0">
```

| Name   | Type  | Description                                          |
|:------:|:-----:|:-----------------------------------------------------|
| Number | Int   | Number of the category in the list.                  |

## 4.1.2. Category name, \<Name\>

```xml
<Name>'SOP, SOIC</Name>
```

| Name   | Type  | Description                                          |
|:------:|:-----:|:-----------------------------------------------------|
| Name   | Text  | Category name.                                       |

## 4.1.3. List of category types, \<Types\>

```xml
<Types>  – start of the list of types;
{...}    – list of types (Type);
</Types> – end of the list of types.
```

## 4.1.3.1. Type description, \<Type\>

## 4.1.3.1.1. Type number

```xml
<Type Number="2">
```

| Name   | Type  | Description                                          |
|:------:|:-----:|:-----------------------------------------------------|
| Number | Int   | Type number in the list of the current category.     |

## 4.1.3.1.2. Type name

```xml
<Name>SOP, SOIC</Name>
```

| Name   | Type  | Description                                          |
|:------:|:-----:|:-----------------------------------------------------|
| Name   | Text  | Type name.                                           |

## 4.1.3.1.3. List of SubTypes, \<SubTypes\>

```xml
<SubTypes>  – start of the list of subtypes;
{...}       – list of subtypes (SubType);
</SubTypes> – end of the list of subtypes.
```

## 4.1.3.1.3.1. Subtype description, \<SubType\>

## 4.1.3.1.3.1.1. Subtype number

```xml
<SubType Number="2">
```

| Name  | Type  | Description                                          |
|:-----:|:-----:|:-----------------------------------------------------|
| Number| Int   | Subtype number in the list of the current type.      |

## 4.1.3.1.3.1.2 Subtype name

```xml
<Name>'SOP, SOIC</Name>
```

| Name  | Type  | Description                                          |
|:-----:|:-----:|:-----------------------------------------------------|
| Name  | Text  | Subtype name.                                       |

## 5. Pattern description, \<Patterns\>

```xml
<Patterns>  – start of the pattern description section;
{...}       – pattern description (Pattern);
</Patterns> – end of the pattern description section.
```

## 5.1.1. Start of the Pattern description, \<Pattern\>

```xml
<Pattern RefDes="RD" Mounting="Chassis" Width="250" Height="400" Orientation="0"
LockTypeChange="N" Type="Free" Float1="0" Float2="0" Float3="0" Int1="0" Int2="0">
```

| Name           | Type   | Description                                                                                |
|:--------------:|:------:|:-------------------------------------------------------------------------------------------|
| RefDes         | Text   | Pattern RefDes                                                                             |
| Mounting       | Text   | Pattern mounting type: "None"; "Through"; "SMD"; "Chassis"; "Mixed".                       |
| Width          | Real   | Pattern width. X distance between the extreme points of objects.                           |
| Height         | Real   | Pattern height. Y distance between the extreme points of objects.                          |
| Orientation    | Text   | Pattern rotation: "0"; "90"; "180"; "270". Rotation does not imply recounting coordinates of objects by angle, rotation value is used just to edit pattern values if Type ≠ "Free". |
| LockTypeChange | Bool   | Lock of pattern template change: "Y" – ON; "N" – OFF.                                     |
| Type           | Text   | Style of the pattern creation template: "Free"; "Circle"; "Lines"; "Square"; "Matrix"; "Rectangle"; "Zig-Zag"; "IPC-7351". |
| Float1        | Real   | Style parameter in the pattern creation template: = 0 for Type = Free; = Radius for Type = Circle; = Pad Spacing for Type = Lines; = Pad Spacing for Type = Square; = X Pad Spacing for Type = Matrix; = Pad Spacing for Type = Rectangle; = Pad Spacing for Type = Zig-Zag; = 0 for Type = IPC-7351. |
| Float2        | Real   | Style parameter in the pattern creation template: = 0 for Type = Free; = 0 for Type = Circle; = Line Spacing for Type = Lines; = Line Spacing for Type = Square; = Y Pad Spacing for Type = Matrix; = Width for Type = Rectangle; = Line Spacing for Type = Zig-Zag; = 0 for Type = IPC-7351. |
| Float3        | Real   | Style parameter in the pattern creation template: = 0 for Type = Free; = 0 for Type = Circle; = 0 for Type = Lines; = 0 for Type = Square; = 0 for Type = Matrix; = Height for Type = Rectangle; = 0 for Type = Zig-Zag; = 0 for Type = IPC-7351. |
| Int1          | Int    | Style parameter in the pattern creation template: = 0 for Type = Free; = Number of Pads for Type = Circle; = Number of Lines for Type = Lines; = Number of Pads for Type = Square; = Columns for Type = Matrix; = Horizontal Pads for Type = Rectangle; = Number of Pads for Type = Zig-Zag; = 1 for Type = IPC-7351. |
| Int2          | Int    | Style parameter in the pattern creation template: = 0 for Type = Free; = 0 for Type = Circle; = Number of Pads for Type = Lines; = 0 for Type = Square; = Rows for Type = Matrix; = Vertical Pads for Type = Rectangle; = 0 for Type = Zig-Zag; = 0 for Type = IPC-7351. |

## 5.1.2. Pattern name, \<Name\>

```xml
<Name>BGA16CP80_4X4_300X300X90B32M</Name>
```

| Name   | Type  | Description                                          |
|:------:|:-----:|:-----------------------------------------------------|
| Name   | Text  | Pattern name.                                        |

## 5.1.3. Pattern name description, \<Name_Description\>

```xml
<Name_Description>BGA (Ball Grid Array), 16 pin, collapsing ball, 0.8mm column pitch x 0.8mm
row pitch, 4 columns x 4 rows, 3mm body length x 3mm body width x 0.9mm height, 0.325mm ball
diameter, most density</Name_Description>
```

| Name   | Type  | Description                                          |
|:------:|:-----:|:-----------------------------------------------------|
| Name   | Text  | Pattern name description.                            |

## 5.1.4. Pattern unique name, \<Name_Unique\>

```xml
<Name_Unique>ROHM_BGA016W030</Name_Unique>
```

## 5.1.5. Pattern value, \<Value\>

```xml
<Value></Value>
```

| Name   | Type  | Description                                          |
|:------:|:-----:|:-----------------------------------------------------|
| Value  | Text  | Pattern value.                                       |

## 5.1.6. Pattern Manufacturer, \<Manufacturer\>

```xml
<Manufacturer>ROHM Semiconductor</Manufacturer>
```

| Name   | Type  | Description                                          |
|:------:|:-----:|:-----------------------------------------------------|
| Manufacturer | Text  | ‘Manufacturer’ field of the pattern.           |

## 5.1.7. Pattern Datasheet link ,\<Datasheet\>

```xml
<Datasheet>http://datasheets.diptrace.com/rohm/bd6874gsw.pdf</Datasheet>
```

| Name      | Type  | Description                                          |
|:---------:|:-----:|:-----------------------------------------------------|
| Datasheet | Text  | Pattern Datasheet link.                              |

## 5.1.8. List of Possible Names of pattern, \<PossibleNames\>

```xml
<PossibleNames>  – start of the list of possible names;
{...}            – list of possible names (PossibleName);
</PossibleNames> – end of the list of possible names.
```

## 5.1.8.1. Pattern Possible Name, \<PossibleName\>

```xml
<PossibleName>CSBGA25</PossibleName>
```

| Name  | Type  | Description                                          |
|:-----:|:-----:|:-----------------------------------------------------|
| Name  | Text  | Possible Name of pattern.                            |

## 5.1.9. Category assigned to pattern, \<Category\>

## 5.1.9.1. Category number in the list, \<Index\>

```xml
<Category Index="0">
```

| Name  | Type  | Description                                                       |
|:-----:|:-----:|:------------------------------------------------------------------|
| Index | Int   | The number of the category assigned to pattern in the list (4.1). |

## 5.1.9.2. Name of the category assigned to pattern, \<Name\>

```xml
<Name>BGA</Name>
```

| Name  | Type  | Description                                                       |
|:-----:|:-----:|:------------------------------------------------------------------|
| Name  | Text  | Name of the category assigned to pattern.                         |

## 5.1.9.3. List of types and subtypes assigned to pattern, \<CategoryTypes\>

```xml
<CategoryTypes>  – start of the list of types and subtypes;
{...}            – list of types and subtypes (CategoryType);
</CategoryTypes> – end of the list of list of types and subtypes.
```

## 5.1.9.3.1. Type and Subtype description, \<CategoryType\>

## 5.1.9.3.1.1. Type name and number, \<Type\>

```xml
<Type Index="4">'Pitch 1.27mm</Type>
```

| Name  | Type  | Description                                          |
|:-----:|:-----:|:-----------------------------------------------------|
| Index | Int   | Type number in the current category list.            |
| Text  | Text  | Type name.                                           |

## 5.1.9.3.1.2. SubType name and number, \<SubType\>

```xml
<SubType Index="1">CTT332</SubType>
```

| Name  | Type  | Description                                          |
|:-----:|:-----:|:-----------------------------------------------------|
| Index | Int   | Subtype number in the current type list.             |
| Text  | Text  | Subtype name.                                        |

## 5.1.10. Pattern Origin parameters, \<Origin\>

```xml
<Origin X="-1.95" Y="0.35" Cross="Y" Circle="Y" Common="Hide" Courtyard="Show"/>
```

| Name    | Type  | Description                                                                                     |
|:-------:|:-----:|:------------------------------------------------------------------------------------------------|
| X      | Real  | X coordinate of Origin. X distance from pattern center coordinate (0;0) to the Origin coordinate.|
| Y      | Real  | Y coordinate of Origin. Y distance from pattern center coordinate (0;0) to the Origin coordinate.|
| Cross   | Bool  | "Y" – show cross in the origin.                                                                |
| Circle  | Bool  | "Y" – show circle in the origin (cross+circle make target).                                    |
| Common  | Text  | Show origin in all layers: "Show"; "Hide"; "Show if not center" (not used at the moment).     |
| Courtyard | Text | Show origin in courtyard layer: "Show"; "Hide".                                               |

## 5.1.11. Pattern Recovery Code, \<RecoveryCode\>

```xml
<RecoveryCode Generator="Y" Model="Y">[Y;BGA;1;N;Y;0;0;0;Y;Y;N;N;101;Default;|
0;0;4;0.8;;4;4;;;;;0.9;0.325;;;;;3;-0.1;0.1;2.9;3.1;3;-0.1;0.1;2.9;3.1;0.26|
0;|;;;;;;;;0.325;0.325;0.325||||||||||||||4934475;15461355;16119285;Y]</RecoveryCode>
```

| Name      | Type  | Description                                                                                     |
|:---------:|:-----:|:------------------------------------------------------------------------------------------------|
| Generator | Bool  | use code to generate pattern.                                                                  |
| Model     | Bool  | use code to generate 3D model.                                                                 |
| [...]     | Text  | Code set by DT IPC-7351 pattern generator; empty for others.                                   |

## 5.1.12. Pattern groups list, \<Groups\>

```xml
<Groups>  – start of the list of groups;
{...}     – group descriptions (Group);
</Groups> – end of the list of groups.
```

## 5.1.12.1. Pattern group description \<Group\>

```xml
<Group Id="0" X="0.26" Y="1.905"/>
```

| Name  | Type  | Description                                          |
|:-----:|:-----:|:-----------------------------------------------------|
| Id    | Int   | Id (unique number) of the group in pattern.         |
| X     | Real  | X coordinate of the center of the rectangle enclosing all elements of the group. |
| Y     | Real  | Y coordinate of the center of the rectangle enclosing all elements of the group. |

## 5.1.13. List of Additional Fields, \<AddFields\>

```xml
<AddFields Type="Text">  – start of the list of Additional Fields;
{...}        – list of Additional Fields (AddField);
</AddFields> – end of the list of Additional Fields.
```

| Name  | Type  | Description                                          |
|:-----:|:-----:|:-----------------------------------------------------|
| Type  | Text  | Additional field value type: "Text"; "Link".         |

## 5.1.13.1. Additional Field Description, \<AddField\>

## 5.1.13.1.1. Additional Field Type

## 5.1.13.1.2. Additional Field Name (Name), \<Name\>

```xml
<Name></Name>
```

| Name  | Type  | Description                                          |
|:-----:|:-----:|:-----------------------------------------------------|
| Name  | Text  | Additional Field Name.                               |

## 5.1.13.1.3. Additional Field Value (Value), \<Text\>

```xml
<Text></Text>
```

| Name  | Type  | Description                                          |
|:-----:|:-----:|:-----------------------------------------------------|
| Text  | Text  | Additional Field Value.                              |

## 5.1.14. Supplier Details, \<Suppliers\>

```xml
<Suppliers>  – start of the supplier details;
{...}        – supplier details (PartNumber, Manufacturer, Pattern, Supplier, Currency);
</Suppliers> – end of the supplier details.
```

## 5.1.14.1. Supplier search string, \<PartNumber\>

```xml
<PartNumber>KPT-2012SYCK</PartNumber>
```

| Name       | Type  | Description                                          |
|:----------:|:-----:|:-----------------------------------------------------|
| PartNumber | Text  | Part Number string for search.                       |

## 5.1.14.2. Manufacturer, \<Manufacturer\>

```xml
<Manufacturer>Kingbright</Manufacturer>
```

| Name         | Type  | Description                                          |
|:------------:|:-----:|:-----------------------------------------------------|
| Manufacturer | Text  | Manufacturer Text Manufacturer.                      |

## 5.1.14.3. Pattern name for search, \<Pattern\>

```xml
<Pattern>0805</Pattern>
```

| Name    | Type  | Description                                          |
|:-------:|:-----:|:-----------------------------------------------------|
| Pattern | Text  | Pattern name for search.                             |

## 5.1.14.4. Supplier, \<Supplier\>

```xml
<Supplier>Distrelec</Supplier>
```

| Name     | Type  | Description                                          |
|:--------:|:-----:|:-----------------------------------------------------|
| Supplier | Text  | Supplier Text Supplier name.                         |

## 5.1.14.5. Currency, \<Currency\>

```xml
<Currency>eur</Currency>
```

| Name     | Type  | Description                                          |
|:--------:|:-----:|:-----------------------------------------------------|
| Currency | Text  | Preferred currency.                                  |

## 5.1.15. Default Pad Style, \<DefPad\>

```xml
<DefPad Style="PadT7"/>
```

| Name  | Type  | Description                                          |
|:-----:|:-----:|:-----------------------------------------------------|
| Style | Text  | Default Pad Style = PadStyle Name in the Pad Style description section, \<PadStyles\> (Section 3). |

## 5.1.16. Start of the list of pads, \<Pads\>

```xml
<Pads>  – start of the list of pads;
{...}   – list of pads (Pad);
</Pads> – end of the list of pads.
```

## 5.1.16.1.1. Pad description, \<Pad\>

```xml
<Pad Id="1" Style="PadT7" X="-0.7849" Y="5.2299" Angle="0" Locked="N" Side="Top"
Group="0">
```

| Name   | Type  | Description                                                                                     |
|:------:|:-----:|:------------------------------------------------------------------------------------------------|
| Id     | Int   | Pad Id (unique number) in the pattern.                                                         |
| Style  | Text  | Pad Style (PadStyle Name) from the list \<PadStyles\> (Section 3).                             |
| X      | Real  | X coordinate. The X distance from the pattern center coordinate (0;0) to the pad center coordinate. |
| Y      | Real  | Y coordinate. The Y distance from the pattern center coordinate (0;0) to the pad center coordinate. |
| Angle  | Real  | Pad rotation in radians, counterclockwise.                                                     |
| Locked | Bool  | Pad change lock: "N" – OFF: pad change allowed; "Y" – ON: pad change locked.                   |
| Side   | Text  | Pad location side: "Top" – on the top side (in the Top layer); "Bottom" – on the bottom side (in the Bottom layer). |
| Group  | Int   | Group number inside pattern, see \<Pattern_Groups\>.                                                                 |

## 5.1.16.1.2. Pad Number (Number field of pad), \<Number\>

```xml
<Number>A1</Number>
```

| Name   | Type  | Description                                          |
|:------:|:-----:|:-----------------------------------------------------|
| Number | Text  | Number field of the pad.                             |

## 5.1.16.1.3. Pad description (Note field), \<Note\>

```xml
<Note></Note>
```

| Name   | Type  | Description                                          |
|:------:|:-----:|:-----------------------------------------------------|
| Note   | Text  | Note Text Note field of the pad.                             |

## 5.1.17. Start of the list of pattern shapes and texts \<Shapes\>

```xml
<Shapes>  – start of the list of pattern shapes and texts;
{...}     – list of pattern shapes and texts (Shape);
</Shapes> – end of the list of pattern shapes and texts.
```

## 5.1.17.1. Shape description \<Shape\>

```xml
<Shape Id="1" Type="Text" Locked="N" Layer="Top Silk" FontVector="Y" FontName="Tahoma"
FontSize="8" FontScale="1" FontWidth="-2" TextShow="Any Text" HorzAlign="Left"
VertAlign="Top" TextAlign="Left" LineSpacing="1.2" Angle="0" AllLayers="N" Group="1">
    <Points>
        <Item X="-1.3488" Y="-1.5"/>
        <Item X="1.6512" Y="1.5"/>
    </Points>
    <TextLines/>
</Shape>
```

## 5.1.17.1.1. Main parameters of Shape \<Shape\>

| Name      | Type  | Description                                                                                     |
|:---------:|:-----:|:------------------------------------------------------------------------------------------------|
| Id       | Int   | Shape Id (unique number) in the pattern.                                                       |
| Type     | Text  | Shape type: "Line"; "Rectangle"; "Obround"; "FillRectangle"; "FillObround"; "Arc"; "Text"; "Polyline"; "Polygon". |
| Locked   | Bool  | Change lock: "Y" – ON, changes locked; "N" – OFF, changes allowed.                            |
| Layer    | Text  | Shape layer: "Top Silk"; "Top Assy"; "Top Mask"; "Top Paste"; "Bottom Paste"; "Bottom Mask". "Bottom Assy"; "Bottom Silk"; "Top"; "Top Keepout"; "Bottom Keepout"; "Bottom"; "Board Cutout"; "Top Dimension"; "Bottom Dimension"; "Non-Signal"; "Top Courtyard"; "Bottom Courtyard"; "Top Outline"; "Bottom Outline"; "Top Terminals"; "Bottom Terminals". |
| FontVector| Bool | "Y" – vector font; "N" – True Type font.                                                            |
| FontName | Text  | Name of the TrueType font.                                                                    |
| FontSize | Int   | Font size.                                                                                    |
| FontScale| Real  | Horizontal scale for the vector text.                                                        |
| FontWidth| Real  | Line width for vector text: -3 – thin; -2 – normal; -1 – bold; >0 – custom, actual value is set here. |
| TextShow | Text  | Displayed text: "Any Text"; "Name"; "RefDes"; "Value"; "Manufacturer"; "Unique Name"; "Datasheet". |
| HorzAlign| Text  | Horizontal text anchor point: "Center"; "Right"; "Left".                                               |
| VertAlign| Text  | Vertical text anchor point: "Center"; "Bottom"; "Top".                                               |
| TextAlign| Text  | Text alignment: "Center"; "Right"; "Left".                                               |
| LineSpacing| Real| Line spacing for multiline text.                                                            |
| Angle    | Real  | Angle of the text in radians, counterclockwise.                                             |
| LineWidth| Real  | Custom Line width for shapes where lines exist (not filled shapes, not text). The parameter is absent if the ‘Use common line width for layer’ option is enabled. |
| AllLayers| Bool  | "Y" – shape is located in all signal layers, applied to signal layers; "N" – shape is located in the specific layer. |
| Group    | Int   | Group number inside pattern, see \<Pattern_Groups\> section.                                 |

## 5.1.17.1.2. List of lines of "Text" shape, \<Lines\>

```xml
<Lines>  – start of the list of lines;
{...}    – list of lines (Item);
</Lines> – end of the list of lines.
```

## 5.1.17.1.2.1. Lines of "Text" shape, \<Item\>

```xml
<Item>Segm</Item>
```

| Name   | Type  | Description                                          |
|:------:|:-----:|:-----------------------------------------------------|
| Item   | Text  | Item Text Text line.                              |

## 5.1.17.1.3. List of shape points, \<Points\>

```xml
<Points>  – start of the list of shape points;
{...}     – list of shape points (Item);
</Points> – end of the list of shape points.
```

## 5.1.17.1.3.1. Shape point coordinates, \<Item\>

```xml
<Item X="-31.4367" Y="23.9103"/>
```

| Name   | Type  | Description                                          |
|:------:|:-----:|:-----------------------------------------------------|
| X      | Real  |  X coordinate.                                       |
| Y      | Real  | Y coordinate.                                        |

## 5.1.18. List of mounting holes \<Holes\>

```xml
<Holes>  – start of the list of mounting holes;
{...}    – list of mounting holes (Hole);
</Holes> – end of the list of mounting holes.
```

## 5.1.18.1. Mounting hole description, \<Hole\>

```xml
<Hole Id="1" Locked="Y" X="-7.1982" Y="1.3482" Diam="2" HoleDiam="1" Group="0"/>
```

| Name   | Type  | Description                                          |
|:------:|:-----:|:-----------------------------------------------------|
| Id     | Int   | Id (unique number) of the hole in the pattern.      |
| Locked | Bool  | Hole change lock: "N" – OFF: hole change allowed; "Y" – ON: hole change locked.                        |
| X      | Real  | X coordinate. X distance from the pattern centre coordinate (0;0) to the hole centre coordinate. |
| Y      | Real  | Y coordinate. Y distance from the pattern centre coordinate (0;0) to the hole centre coordinate. |
| Diam   | Real  | Keepout area diameter.                               |
| HoleDiam| Real | Hole diameter.                                       |
| Group  | Int   | Group number inside pattern, see \<Pattern_Groups\>.                         |

## 5.1.19. List of dimensions, \<Dimensions\>

```xml
<Dimensions> – start of the list of dimensions;
{...} – list of dimensions (Dimension);
</Dimensions> – end of the list of dimensions.
```

## 5.1.19.1. Dimension description, \<Dimension\>

## 5.1.19.1.1. Dimension main parameters, \<Dimension\>

```xml
<Dimension Locked="N" Type="Horizontal" Connected1="Pad" Object1="0" SubObject1="1"
Point1="0" Connected2="None" Object2="0" SubObject2="0" Point2="0" Layer="Top Dimension"
X1="-5.9282" Y1="5.1582" X2="-2.1182" Y2="5.1582" XD="-5.9282" YD="7.6982"
ArrowSize="0.6667" Units="Common" FontVector="Y" FontName="Tahoma" FontSize="2"
FontScale="1" FontWidth="-2" ShowUnits="N" Angle="0" ExternalRadius="0" PointerMode="0"
Group="0"/>
```

| Name      | Type  | Description                                                                                     |
|:---------:|:-----:|:------------------------------------------------------------------------------------------------|
| Locked    | Bool  | Resize lock: "N" – OFF: resizing allowed; "Y" – ON: resizing locked.                          |
| Type      | Text  | Dimension Type: "Horizontal"; "Vertical"; "Free"; "Radius"; "Pointer".                        |
| Connected1 | Text  | The type of the object to which the first point of the dimension is attached: "None"; "Pad"; "Shape"; "Hole"; "Terminal". |
| Object1   | Int   | For Connected1="Terminal" – sequence number of the pad in the list. See \<Pads\>.          |
| SubObject1| Int   | Sequence number of the object in the corresponding array.                             |               |
| Point1    | Int   | Number of the object anchor point to which the first dimension point is connected.                      |
| Connected2 | Text | The type of object to which the second dimension point is connected: "None"; "Pad"; "Shape"; "Hole"; "Terminal". |
| Object2   | Int   | For Connected2="Terminal" – sequence number of the pad in the list. See \<Pads\>.          |
| SubObject2| Int   | Sequence number of the object in the corresponding array.                             |               |
| Point2    | Int   | Number of the object anchor point to which the second dimension point is connected.                     |
| Layer     | Text  | Dimension layer: "Top Dimension"; "Bottom Dimension".                                               |
| X1        | Real  | The X coordinate of the first dimension point. The X distance from the pattern centre coordinate (0;0) to the first dimension point. |
| Y1        | Real  | The Y coordinate of the first dimension point. The Y distance from the pattern centre coordinate (0;0) to the first dimension point. |
| X2        | Real  | The X coordinate of the second dimension point. The X distance from the pattern centre coordinate (0;0) to the second dimension point. |
| Y2        | Real  | The Y coordinate of the second dimension point. The Y distance from the pattern centre coordinate (0;0) to the second dimension point. |
| XD        | Real  | The X coordinate of the first point of the dimension line. The X distance from the pattern centre coordinate (0;0) to the first dimension point. |
| YD        | Real  | The Y coordinate of the first point of the dimension line. The Y distance from the pattern centre coordinate (0;0) to the first dimension point. |
| ArrowSize | Real  | Dimension line arrow length.                                                                |
| Units     | Text  | Dimension measuring units: "Common"; "inch"; "mil"; "mm".                                 |
| FontVector| Bool  | "Y" – vector font; "N" – True Type font.                                                            |
| FontName  | Text  | Name of TrueType font.                                                                    |
| FontSize  | Int   | Font size.                                                                                    |
| FontScale | Real  | Horizontal scale for vector text.                                                        |
| FontWidth | Real  | Line width for vector text: -3 – thin; -2 – normal; -1 – bold; >0 – custom, actual value is set here. |
| ShowUnits | Bool  | "Y" – show measurement units; "N" – do not show measurement units.                          |
| Angle     | Real  | Angle of the dimension line.                                                             |
| ExternalRadius | Int | Arc direction, actual for Type="Radius": 1 – inside circumference; -1 – outside circumference; 0 – for other Type. |
| PointerMode| Int  | Actual for Type="Pointer". Show: 0 – Coordinates; 1 – Text.                                      |
| Group     | Int   | Group number inside pattern, see \<Pattern_Groups\>.                                 |

## 5.1.19.1.2. Text for Pointer

```xml
<PointerText>DimComment</PointerText>
```

| Name   | Type  | Description                                          |
|:------:|:-----:|:-----------------------------------------------------|
| PointerText | Text | Pointer text, if Type="Pointer".                   |

## 5.1.20. Pattern 3D model, \<Model3D\>

```xml
<Model3D Mirror="N" NoSearch="N" Units="Wings" IPC_XOff="-0.483393"
IPC_YOff="0.103078" AutoHeight="0" AutoColor="4934475" Type="File" KeepPins="N">
```

| Name     | Type  | Description                                          |
|:--------:|:-----:|:-----------------------------------------------------|
| Mirror   | Bool  | "Flip by Z Axis” check box status: "Y" – enabled; "N" – disabled.|
| NoSearch  | Bool  | "Turn Off Automatic Search” check box status: "Y" – enabled; "N" – disabled.          |
| Units    | Text  | Units used for loading model file: "mm" – meters; "mil" – mils; "inch" – inch; "Wings" – Wings system.          |
| IPC_XOff | Real  | Shift of IPC-7351 model in X-direction, changed automatically when pattern is centered/edited. |
| IPC_YOff | Real  | Shift of IPC-7351 model in Y-direction, changed automatically when pattern is centered/edited. |
| AutoHeight| Real | Height of the model if it is built by component outline. |
| AutoColor | Int  | Color of the model built by component outline.        |
| Type     | Int   | Model type: "File" – loading model from file; "IPC-7351" – IPC-7351 model (generated automatically by IPC recovery code); "Outline" – generated by component outline with specified autoheight. |
| KeepPins | Bool  | "Keep All Model Pins” checkbox status: "Y" – enabled (keep all pins of IPC7351 model); "N" – disabled (remove pins outside pads). |

## 5.1.20.1. Model filename, \<Filename\>

```xml
<Filename>
<Path>C:\Program Files (x86)\DipTrace\models3d\DIP Peg Leads\dip-10(16)s.step</Path>
<Var>C:\Program Files (x86)\DipTrace\models3d\DIP Peg Leads\dip-10(16)s.step</Var>
</Filename>
```

| Name  | Type  | Description                                          |
|:-----:|:-----:|:-----------------------------------------------------|
| Path  | Text  | Name of the model file.                              |
| Var   | Text  | The name of the model file, expressed as an environment variable, if any. |

## 5.1.20.2. Model rotation, \<Rotate\>

```xml
<Rotate X="0" Y="0" Z="0"/>
```

| Name  | Type  | Description                                          |
|:-----:|:-----:|:-----------------------------------------------------|
| X     | Real  | The angle of rotation of the model in X-direction (in degrees). |
| Y     | Real  | The angle of rotation of the model in Y-direction (in degrees). |
| Z     | Real  | The angle of rotation of the model in Z-direction (in degrees, negative value of the set one). |

## 5.1.20.3. Model shift, \<Offset\>

```xml
<Offset X="0" Y="0" Z="0"/>
```

| Name  | Type  | Description                                          |
|:-----:|:-----:|:-----------------------------------------------------|
| X     | Real  | Model offset in X-direction.                         |
| Y     | Real  | Model offset in Y-direction.                         |
| Z     | Real  | Model offset in Z-direction (negative value of the set one). |

## 5.1.20.4. Model scale, \<Zoom\>

```xml
<Zoom X="1" Y="1" Z="1"/>
```

| Name  | Type  | Description                                          |
|:-----:|:-----:|:-----------------------------------------------------|
| X     | Real  | X-axis model scaling factor.                         |
| Y     | Real  | Y-axis model scaling factor.                         |
| Z     | Real  | Z-axis model scaling factor.                         |
