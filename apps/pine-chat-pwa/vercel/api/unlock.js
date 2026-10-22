import { timingSafeEqual } from "node:crypto";
import { grant,json } from "../lib/session.js";
const tries=new Map();
export default async function handler(req,res){
 if(req.method!=="POST")return json(res,405,{error:"method_not_allowed"});
 const origin=req.headers.origin;
 if(origin && origin!=="https://"+req.headers.host)return json(res,403,{error:"origin_denied"});
 const ip=String(req.headers["x-forwarded-for"]||req.socket?.remoteAddress||"unknown").split(",")[0].slice(0,80);
 const now=Date.now(),old=tries.get(ip);
 if(old && old.until>now && old.count>=5){res.setHeader("Retry-After",String(Math.ceil((old.until-now)/1000)));return json(res,429,{error:"rate_limited"});}
 const pin=req.body?.pin,expected=process.env.PINE_APP_PIN;
 if(!expected||!process.env.PINE_APP_SESSION_KEY)return json(res,503,{error:"service_unavailable"});
 const okay=typeof pin==="string"&&/^\d{4}$/.test(pin)&&timingSafeEqual(Buffer.from(pin.padEnd(4)),Buffer.from(expected.padEnd(4)));
 if(!okay){
   tries.set(ip,old && old.until>now?{count:old.count+1,until:old.until}:{count:1,until:now+15*60*1000});
   return json(res,401,{error:"invalid_pin"});
 }
 tries.delete(ip);grant(res);return json(res,200,{authenticated:true,expires_in:28800});
}