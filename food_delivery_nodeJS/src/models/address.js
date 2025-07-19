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
    city: {
        type: String,
        required: true
    },
    state: {
        type: String,
        required: true
    },
    pincode: {
        type: String,
        required: true
    }
}, {timestamps:true})

module.exports =mongoose.model('Address',addressSchema)