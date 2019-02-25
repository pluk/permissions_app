import axios from 'axios';

export default class ApiClient {
    constructor(APIHost) {
        this.APIHost = APIHost;
        this.config = {'headers': {}};
    }


    get (resource, params = '') {
        return axios.get(this.APIHost + resource + '?' + params, this.config);
    }

    put (resource, payload) {
        return axios.put(this.APIHost + resource, payload, this.config);
    }
}