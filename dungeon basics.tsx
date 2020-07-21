<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.4" tiledversion="1.4.1" name="dungeon basics" tilewidth="16" tileheight="16" tilecount="256" columns="16">
 <image source="dungeon_basics_source/0x72_16x16DungeonTileset.v3.png" trans="000000" width="256" height="256"/>
 <tile id="152">
  <properties>
   <property name="animation" value="10"/>
  </properties>
  <animation>
   <frame tileid="153" duration="201"/>
   <frame tileid="154" duration="201"/>
   <frame tileid="155" duration="201"/>
   <frame tileid="156" duration="201"/>
   <frame tileid="157" duration="201"/>
   <frame tileid="158" duration="201"/>
   <frame tileid="159" duration="201"/>
  </animation>
 </tile>
 <tile id="168">
  <properties>
   <property name="animation" value="10"/>
  </properties>
 </tile>
 <tile id="190">
  <objectgroup draworder="index" id="2">
   <object id="1" name="chest" x="0.0601504" y="1.92481" width="15.9398" height="14.1955"/>
  </objectgroup>
 </tile>
 <tile id="191">
  <animation>
   <frame tileid="152" duration="100"/>
   <frame tileid="168" duration="100"/>
  </animation>
 </tile>
 <tile id="223">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="16.1805" height="15.9398"/>
  </objectgroup>
 </tile>
</tileset>
