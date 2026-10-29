"use client";
import "./brand-charts.css";
import React, { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart";
import { ResponsiveContainer, LineChart, Line, BarChart, Bar, AreaChart, Area, PieChart, Pie, Cell, CartesianGrid, XAxis, YAxis, Tooltip } from "recharts";

export const palettes = [
 {name:"Florentine · original",bg:"#F3EDE1",fg:"#20231F",muted:"#685F52",grid:"#D8D0C1",colors:["#103F35","#B99A58","#6B303D","#88715B"]},
 {name:"Florentine · sharper light",bg:"#F3EDE1",fg:"#20231F",muted:"#685F52",grid:"#D8D0C1",colors:["#08745C","#A52F50","#4655BB","#B97808"]},
 {name:"Phthalo · luminous",bg:"#082E28",fg:"#F3EDE1",muted:"#B6C8BD",grid:"#31534A",colors:["#35E8B5","#FFC247","#F47798","#9BAAFF"]},
 {name:"Ink · Florentine",bg:"#20231F",fg:"#F3EDE1",muted:"#C2BBAE",grid:"#45483F",colors:["#35E8B5","#FFC247","#F47798","#9BAAFF"]}
];
const data = [
 {day:"Sep 7",organic:64,paid:32,revenue:120}, {day:"Sep 10",organic:92,paid:68,revenue:165},
 {day:"Sep 13",organic:78,paid:46,revenue:148}, {day:"Sep 16",organic:112,paid:72,revenue:210},
 {day:"Sep 19",organic:86,paid:52,revenue:190}, {day:"Sep 22",organic:138,paid:94,revenue:280},
 {day:"Sep 25",organic:105,paid:70,revenue:235}, {day:"Sep 28",organic:152,paid:116,revenue:320},
 {day:"Oct 1",organic:130,paid:88,revenue:305}, {day:"Oct 4",organic:176,paid:132,revenue:390}
];
const channels = [{name:"Search",value:48},{name:"Direct",value:27},{name:"Social",value:17},{name:"Referral",value:8}];

const fontPairings = [
 {name:"Orbitron · Cortex futuristic",display:"Orbitron",body:"Geist",mono:"Geist Mono"},
 {name:"Space Grotesk · technical editorial",display:"Space Grotesk",body:"Geist",mono:"Geist Mono"},
 {name:"Sora · geometric modern",display:"Sora",body:"Geist",mono:"Geist Mono"},
 {name:"IBM Plex · research journal",display:"IBM Plex Sans",body:"IBM Plex Sans",mono:"IBM Plex Mono"},
 {name:"Newsreader · Renaissance editorial",display:"Newsreader",body:"Geist",mono:"Geist Mono"}
];

export default function BrandCharts() {
 const [index,setIndex]=useState(0);
 const [fontIndex,setFontIndex]=useState(0);
 const f=fontPairings[fontIndex];
 const p=palettes[index];
 const config={organic:{label:"Organic",color:p.colors[0]},paid:{label:"Paid",color:p.colors[1]},revenue:{label:"Revenue",color:p.colors[0]}};
 const axis={tick:{fill:p.muted,fontSize:12},tickLine:false,axisLine:false,minTickGap:32};
 const grid=React.createElement(CartesianGrid,{stroke:p.grid,vertical:false});
 const x=React.createElement(XAxis,{...axis,dataKey:"day",interval:"preserveStartEnd"});
 const y=React.createElement(YAxis,{...axis,width:44});
 const tip=React.createElement(ChartTooltip,{content:React.createElement(ChartTooltipContent),contentStyle:{background:p.bg,color:p.fg,borderColor:p.grid}});
 const legend=(items)=>React.createElement("div",{className:"bc-legend"},items.map(([label,color])=>React.createElement("span",{key:label},React.createElement("i",{style:{background:color}}),label)));
 const panel=(title,unit,chart,labels,wide=false)=>React.createElement(Card,{className:`bc-card ${wide?"bc-wide":""}`,style:{background:p.bg,color:p.fg,borderColor:p.grid},key:title},
 React.createElement(CardHeader,null,React.createElement(CardTitle,{className:"bc-title"},title),React.createElement("div",{className:"bc-unit",style:{color:p.muted}},unit)),
 React.createElement(CardContent,null,React.createElement(ChartContainer,{config,className:"bc-chart",style:{height:240,width:"100%"}},chart),legend(labels)));
 return React.createElement("div",{className:"bc-root",style:{"--bc-display":`"${f.display}",sans-serif`,"--bc-body":`"${f.body}",sans-serif`,"--bc-mono":`"${f.mono}",monospace`,"--bc-bg":p.bg,"--bc-fg":p.fg,"--bc-grid":p.grid,"--background":p.bg,"--foreground":p.fg,"--muted-foreground":p.muted,"--border":p.grid,"--popover":p.bg,"--popover-foreground":p.fg}},
 React.createElement("div",{className:"bc-toolbar"},React.createElement("label",null,"Palette ",React.createElement("select",{value:index,onChange:e=>setIndex(Number(e.target.value)),"aria-label":"Chart palette"},palettes.map((v,i)=>React.createElement("option",{value:i,key:v.name},v.name)))),
 React.createElement("label",null,"Font pairing ",React.createElement("select",{value:fontIndex,onChange:e=>setFontIndex(Number(e.target.value)),"aria-label":"Font pairing"},fontPairings.map((v,i)=>React.createElement("option",{value:i,key:v.name},v.name))))),
 React.createElement("section",{className:"bc-specimen",style:{background:p.bg,color:p.fg,border:`1px solid ${p.grid}`}},
 React.createElement("small",null,`${f.display} · Display / 700`),React.createElement("h1",null,"Florentine Futures"),
 React.createElement("small",null,`${f.body} · Body / 400`),React.createElement("p",null,"Clear thinking. Precise systems. A warmer kind of technology."),
 React.createElement("small",null,`${f.mono} · Data / 500`),React.createElement("p",{className:"bc-numbers",style:{color:p.fg}},"$24,680.00  +18.4%")),
 React.createElement("div",{className:"bc-swatches",style:{background:p.bg,color:p.fg}},[p.bg,p.fg,...p.colors].map((color,i)=>React.createElement("span",{key:i},React.createElement("i",{style:{background:color,border:`1px solid ${p.muted}`}}),React.createElement("code",null,color)))),
 React.createElement("div",{className:"bc-grid"},
 panel("Acquisition over time","Installs · synthetic sample data",React.createElement(LineChart,{data,margin:{top:12,right:16,bottom:0,left:0}},grid,x,y,tip,React.createElement(Line,{dataKey:"organic",stroke:p.colors[0],strokeWidth:3,dot:false,isAnimationActive:false}),React.createElement(Line,{dataKey:"paid",stroke:p.colors[1],strokeWidth:3,strokeDasharray:"7 4",dot:false,isAnimationActive:false})),[["Organic — solid",p.colors[0]],["Paid — dashed",p.colors[1]]],true),
 panel("Install mix","Installs · by date",React.createElement(BarChart,{data,margin:{top:12,right:12,bottom:0,left:0}},grid,x,y,tip,React.createElement(Bar,{dataKey:"organic",stackId:"a",fill:p.colors[0],isAnimationActive:false}),React.createElement(Bar,{dataKey:"paid",stackId:"a",fill:p.colors[1],radius:[3,3,0,0],isAnimationActive:false})),[["Organic",p.colors[0]],["Paid",p.colors[1]]]),
 panel("Revenue trend","Revenue · USD",React.createElement(AreaChart,{data,margin:{top:12,right:12,bottom:0,left:0}},grid,x,y,tip,React.createElement(Area,{dataKey:"revenue",stroke:p.colors[0],fill:p.colors[0],fillOpacity:0.16,strokeWidth:3,isAnimationActive:false})),[["Revenue",p.colors[0]]]),
 panel("Traffic share","Share of sessions · %",React.createElement(PieChart,null,React.createElement(Tooltip,{contentStyle:{background:p.bg,color:p.fg,borderColor:p.grid}}),React.createElement(Pie,{data:channels,dataKey:"value",nameKey:"name",innerRadius:60,outerRadius:92,paddingAngle:3,stroke:"none",isAnimationActive:false},channels.map((v,i)=>React.createElement(Cell,{key:v.name,fill:p.colors[i]})))),channels.map((v,i)=>[`${v.name} ${v.value}%`,p.colors[i]])),
 panel("Channel conversion","Conversion rate · %",React.createElement(BarChart,{data:channels.map(v=>({...v,rate:v.value/10})),layout:"vertical",margin:{top:12,right:20,bottom:0,left:12}},React.createElement(CartesianGrid,{stroke:p.grid,horizontal:false}),React.createElement(XAxis,{...axis,type:"number",domain:[0,6],unit:"%"}),React.createElement(YAxis,{...axis,type:"category",dataKey:"name",width:64,interval:0}),React.createElement(Tooltip,{contentStyle:{background:p.bg,color:p.fg,borderColor:p.grid},formatter:v=>[`${v}%`,"Conversion"]}),React.createElement(Bar,{dataKey:"rate",fill:p.colors[2],radius:[0,3,3,0],isAnimationActive:false})),[["Conversion",p.colors[2]]])
 ));
}
