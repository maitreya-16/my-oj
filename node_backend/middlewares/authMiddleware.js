const jwt = require('jsonwebtoken');
require('dotenv').config();

const auth = (req,res,next)=>{
    console.log("Cookies",req?.cookies);
    if(!req.cookies||!req.cookies.token){
        return res.status(403).json({error:'Access denied'});
    }

const token = req.cookies.token;

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
