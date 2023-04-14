import React from 'react';
import Login from "./Components/Login/index";
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import {Provider} from 'react-redux';
import store from './store/store'
import CurrencyTable from "./Components/CurrencyTable";

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function App() {
  return (
      <Provider store={store}>
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
       <CurrencyTable/>
      </ThemeProvider>
      </Provider>
  );
}

export default App;
