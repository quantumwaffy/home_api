import axios from "axios";
import urlJoin from 'url-join';

export type User = {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    roles : {name: string}[];
    disabled: boolean;
    full_name: string;
}

export type AuthHeader = {
    headerName: string;
    headerValue: string;
}


export function getV1Url(endpoint: string) {
    return urlJoin(process.env.REACT_APP_API_V1_PREFIX || "", endpoint)
}

export const getCurrentUser = async (header: AuthHeader, setIsAuth: (state: boolean) => void) => (
    await axios.get(
        getV1Url("auth/me"),
        {headers: {[header.headerName]: header.headerValue}}
    )
        .then(response => {
            setIsAuth(true);
            return response.data;
        })
        .catch(error => setIsAuth(false))
)
