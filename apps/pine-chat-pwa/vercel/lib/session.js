import { createHmac,timingSafeEqual } from "node:crypto";
const MAX_AGE=8*60*60;
export function verify(req){
 const raw=(req.headers.cookie||"").split(";").map(v=>v.trim()).find(v=>v.startsWith("pine_session="))?.slice(13)||"";
 const parts=raw.split(".");
 if(parts.length!==3||parts[0]!=="v1"||!/^\d{10,11}$/.test(parts[1])||!/^[a-f0-9]{64}$/i.test(parts[2]))return false;
 const expiry=Number(parts[1]);const now=Math.floor(Date.now()/1000);
 if(expiry<=now||expiry>now+MAX_AGE)return false;
 const secret=process.env.PINE_APP_SESSION_KEY;
 if(!secret||secret.length<32)return false;
 const calculated=createHmac("sha256",secret).update("pine-chat:v1:"+parts[1]).digest("hex");
 return timingSafeEqual(Buffer.from(calculated),Buffer.from(parts[2]));
}
export function grant(res){
 const secret=process.env.PINE_APP_SESSION_KEY;
 if(!secret||secret.length<32)throw Error("Missing session config");
 const expiry=String(Math.floor(Date.now()/1000)+MAX_AGE);
 const signature=createHmac("sha256",secret).update("pine-chat:v1:"+expiry).digest("hex");
 res.setHeader("Set-Cookie","pine_session=v1."+expiry+"."+signature+"; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age="+MAX_AGE);
}
export function json(res,status,obj){
 res.setHeader("Cache-Control","no-store");res.setHeader("Content-Type","application/json; charset=utf-8");
 return res.status(status).json(obj);
}