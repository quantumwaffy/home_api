import { configureStore } from '@reduxjs/toolkit'
import  authReducer  from './Login/authSlice'

const store = configureStore({
  reducer: {
    auth: authReducer
  }
})
export default store