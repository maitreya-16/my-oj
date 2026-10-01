const jwt = require('jsonwebtoken');
require('dotenv').config();

const auth = (req,res,next)=>{
    const authorization = req.headers.authorization;
    const token = authorization?.match(/^Bearer\s+(\S+)$/i)?.[1];
    if(!token){
        return res.status(403).json({error:'Access denied'});
    }

try{
    const decoded = jwt.verify(token,process.env.JWT_SECRET);
    req.user = decoded;//payload 
    next();
}
catch(error){
if(error.name==='TokenExpiredError'){
    return res.status(401).json({error:'Token expired. Please log in again.'});
}
return res.status(403).json({error:'Invalid token. Please log in again.'});
}

};
module.exports=auth;
