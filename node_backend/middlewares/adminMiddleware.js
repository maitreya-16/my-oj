const jwt = require("jsonwebtoken");
require("dotenv").config();

const adminAuthenticate = (req, res, next) => {
    const authorization = req.headers.authorization;
    const token = authorization?.match(/^Bearer\s+(\S+)$/i)?.[1];
    if (!token) {
        return res.status(403).json({ error: 'Access denied. No token provided.' });
    }

    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        if (decoded.role !== "admin") {
            return res.status(403).json({ error: "Access only For Admins" });
        }
        req.user = decoded;
        next();
    } catch (error) {
        res.status(400).json({ error: "Invalid token", details: error.message });
    }
};

module.exports = adminAuthenticate;