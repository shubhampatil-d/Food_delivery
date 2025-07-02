const mongoose= require('mongoose')

const addressSchema= new mongoose.Schema({
    user:{
        type: String,
        ref: 'User',
        require:true,
    },
    type:{
        type:String,
        enum:['home','work','other'],
        default:"home"
    },
    addressLine:{
        type: String,
        require: true 
    },
    latitude:{
        type: Number,
        require:true 
    },
    longitude:{
        type:Number,
        require:true
    }
}, {timestamps:true})

module.exports =mongoose.model('Address',addressSchema)