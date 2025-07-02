const User =require("../models/user")
const bcrypt =require("bcrypt")
const jwt= require("jsonwebtoken")


exports.register = async (req,res) =>{
    try{
        const {name, phone, email, password} = req.body
        const existing = await User.findOne({email})
        if (existing) {
            return res.status(400).json({error : "email already register"})
        }
        const hashedPassword= await bcrypt.hash(password,10)
        const user = await User.create({
            name, 
            phone,
            email, 
            password: hashedPassword
        })
        res.status(201).json({
            message: "user registered successfully",
            user:{
                id:user._id,
                name:user.name,
                phone: user.phone,
            }
        })
    }catch(err){
        console.error("Register Error:", err)
        res.status(500).json({message: 'server error'})
    }
}


exports.login= async (req, res) =>{
    try {
        const {email, password} = req.body
        const user= await User.findOne({email})
        if (!user) return res.status(404).json({message: "email not found"})
        
        const match = await bcrypt.compare(password, user.password)
        if (!match) return res.status(401).json({message: "incorrect password"})
        
        const token= jwt.sign({id: user._id }, process.env.JWT_SECRET,{expiresIn:'7d'})
        res.json({
            message: "Login successful",
            token, 
            user:{id: user._id, name: user.name, email: user.email}})
    }catch (err){
        res.status(500).json({message: 'server error'})
    }
}