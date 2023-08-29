import mongoose from 'mongoose';
import { MODEL_NAMES} from '../utils/constants.js';

const UserSchema = new mongoose.Schema({
  name: String,
  email: String,
  password: String,
  
  model: {
    type: String,
    enum: Object.values(MODEL_NAMES),
    default: null,
  },
  role: {
    type: String,
    enum: ['user', 'admin'],
    default: 'user',
  },
  avatar: String,
  avatarPublicId: String,
});

UserSchema.methods.toJSON = function () {
  let obj = this.toObject();
  delete obj.password;
  return obj;
};

export default mongoose.model('User', UserSchema);
