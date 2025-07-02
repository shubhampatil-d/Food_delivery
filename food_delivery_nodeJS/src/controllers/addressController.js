const User= require('../models/user')
const Address=require('../models/address')

exports.addAddress= async (req,res) =>{
    try{
        const {addressLine, latitude, longitude, type} = req.body
        const address= await Address.create({
            user: req.user._id,
            type,
            addressLine,
            latitude,
            longitude
        })
        res.status(201).json({message: 'Address added successfully'})
    }catch ( err){
        console.error(err)
        res.status(500).json({message:"Failed to add address"})
    }
}

exports.getAddresses= async (req, res) =>{
    try {
        const addresses= await Address.find({user: req.user._id})
        res.json({addresses})

    } catch(err){
        console.error(err)
        res.status(500).json({message: "Failed to fetch address"})
    }
}

// exports.setDefaultAddress= async (req,res) =>{
//     try{
//         const addressId= req.params.id 
//         const address= await Address.findOne({_id: addressId, user:req.user._id})
//         if (!address){
//             res.status(404).json({message: "address not found"})
//         }
//         await User.findByIdAndUpdate(req.user._id,{defaultAddress:address._id})
//         res.json({message:"default address updated successfully"})

//     }catch(err){
//         console.error(err)
//         res.status(500).json({message: 'Failed to set default address'})
//     }
// }
exports.setDefaultAddress = async (req, res) => {
  try {
    const addressId = req.params.id;

    console.log("User:", req.user);
    console.log("Address ID:", addressId);

    const address = await Address.findOne({
      _id: addressId,
      user: req.user._id,
    });

    if (!address) {
      return res.status(404).json({ message: "Address not found" });
    }

    await User.findByIdAndUpdate(req.user._id, {
      defaultAddress: address._id,
    });

    res.json({ message: "Default address updated successfully" });
  } catch (err) {
    console.error("Error in setDefaultAddress:", err); // 👈 log actual error
    res.status(500).json({ message: "Failed to set default address" });
  }
};

