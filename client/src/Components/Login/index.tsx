import {FC, useState, SyntheticEvent, BaseSyntheticEvent} from "react"
import * as React from 'react';
import TextField from "@mui/material/TextField/TextField";
import FormControl from "@mui/material/FormControl";
import Button from "@mui/material/Button";
import LoginIcon from '@mui/icons-material/Login';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import "./style.css"
import axios from "axios";

const Login: FC  = () => {
    const [tabValue, setTabValue] = useState('base');
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [token, setToken] = useState("");

    const handleTabChange = (event: SyntheticEvent, newValue: string) => {
    setTabValue(newValue);
  };
    const handleUsernameChange = (event:BaseSyntheticEvent) => {
    setUsername(event.target.value);
  };
    const handlePasswordChange = (event:BaseSyntheticEvent) => {
    setPassword(event.target.value);
  };
    const handleTokenChange = (event:BaseSyntheticEvent) => {
    setToken(event.target.value);
  };
    const handleSubmit = (event) => {
        axios.post(
            "/api/v1/auth/login",
            {username: username, password: password},
            {headers: {"Content-Type": 'application/x-www-form-urlencoded'}}
        )
            .then((response) => {
                axios.get("/api/v1/auth/me", {headers: {"Authorization": `Bearer ${response.data.access_token}`}})
                    .then(respMe => console.log(respMe))
            }
            )
            .catch(error => console.log(error))
        event.preventDefault();
    }
    return (
        <FormControl component="form" onSubmit={handleSubmit} className="login-form-wrapper">
            <Box className="login-form-element-wrapper">
              <Tabs
                value={tabValue}
                onChange={handleTabChange}
                textColor="secondary"
                indicatorColor="secondary"
                variant="fullWidth"
              >
                <Tab value="base" label="Base" />
                <Tab value="root" label="Root" />
              </Tabs>
            </Box>
            { tabValue === "base" ?
                <>
                    <TextField
                        className="login-form-element-wrapper"
                        required
                        label="Login"
                        name="login"
                        value={username}
                        onChange={handleUsernameChange}
                    />
                    <TextField
                        className="login-form-element-wrapper"
                        required
                        label="Password"
                        name="password"
                        type="password"
                        value={password}
                        onChange={handlePasswordChange}
                    />
                </>
                :
                <TextField
                    className="login-form-element-wrapper"
                    required
                    label="Token"
                    name="token"
                    type="password"
                    value={token}
                    onChange={handleTokenChange}
                />
            }
            <Button type="submit" className="login-form-element-wrapper" color="secondary" variant="contained" endIcon={<LoginIcon />}>Login</Button>
        </FormControl>

    )
}
export default Login;