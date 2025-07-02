const mongoose = require("mongoose")

const userSchema= new mongoose.Schema({
    name: {
        type : String,
        required: true,
        trim: true
    },
    phone : {
        type: String,
        required: true,
        unique:true,
        match: /^[0-9]{10}$/,
    },
    email:{
        type: String, 
        required: true,
        unique:true,
    },
    password: {
        type: String, 
        required: true},
    
    defaultAddress: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Address'
    }
},{
    timestamps:true
})

module.exports = mongoose.model('User', userSchema)