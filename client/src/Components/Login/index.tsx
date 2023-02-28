import {FC, useState, SyntheticEvent, BaseSyntheticEvent, SetStateAction} from "react"
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
// @ts-ignore
import {getV1Url, getCurrentUser} from "/client/src/utils/api_login.ts";
// @ts-ignore
import type {AuthHeader} from "/client/src/utils/api_login.ts";


enum TabValues {
    ROOT = "root",
    BASE = "base"
}

const Login: FC  = () => {
    const [tabValue, setTabValue] = useState(TabValues.BASE);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [token, setToken] = useState("");
    const [isAuth, setIsAuth] = useState(false);

    const handleTabChange = (event: SyntheticEvent, newValue: SetStateAction<TabValues>) => {
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
    const handleSubmit = async (event: BaseSyntheticEvent) => {
        event.preventDefault();
        if (tabValue === TabValues.BASE) {
            axios.post(
            getV1Url("auth/login"),
            {username: username, password: password},
            {headers: {"Content-Type": 'application/x-www-form-urlencoded'}}
        )
            .then(async (response) => {
                    const accessToken = response.data.access_token;
                    const authHeader: AuthHeader = {
                        headerName: "Authorization",
                        headerValue: `Bearer ${accessToken}`,
                    };
                    const currentUser = await getCurrentUser(authHeader);
                    localStorage.setItem("authHeader", JSON.stringify(authHeader));
                    localStorage.setItem("refreshToken", response.data.refresh_token);
                    localStorage.setItem("user", JSON.stringify(currentUser));
                    setIsAuth(true)
                }
            )
            .catch(error => setIsAuth(false))
        } else if (tabValue === TabValues.ROOT) {
            const authHeader: AuthHeader = {
                headerName: process.env.REACT_APP_SECRET_HEADER_NAME,
                headerValue: token,
            };
            const currentUser = await getCurrentUser(authHeader, setIsAuth);
            localStorage.setItem("authHeader", JSON.stringify(authHeader));
            localStorage.setItem("user", JSON.stringify(currentUser));
            setIsAuth(true);
        }
    }
    console.log(isAuth)
    return (
        <>{
            isAuth ? (
                <TextField
                    className="login-form-element-wrapper"
                    required
                    label="Login"
                    name="login"
                    value={username}
                    onChange={handleUsernameChange}
                />
            ) : (
                <FormControl component="form" onSubmit={handleSubmit} className="login-form-wrapper">
                    <Box className="login-form-element-wrapper">
                      <Tabs
                        value={tabValue}
                        onChange={handleTabChange}
                        textColor="secondary"
                        indicatorColor="secondary"
                        variant="fullWidth"
                      >
                        <Tab value={TabValues.BASE} label="Base" />
                        <Tab value={TabValues.ROOT} label="Root" />
                      </Tabs>
                    </Box>
                    { tabValue === TabValues.BASE ?
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
    </>)
}
export default Login;