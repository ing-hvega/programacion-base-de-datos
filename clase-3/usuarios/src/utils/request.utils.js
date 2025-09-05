import queryString from "querystring";

class Request {
    constructor() {
        this.baseURL = import.meta.env.VITE_BASE_URL;
    }

    get(path, parameters = {}, customHeaders = {}) {
        const params = queryString.stringify(parameters);
        const url = params ? `${path}?${params}` : path;

        return this._makeRequest("GET", url, null, customHeaders);
    }

    post(path, data = null, customHeaders = {}) {
        return this._makeRequest("POST", path, data, customHeaders);
    }

    put(path, data = null, customHeaders = {}) {
        return this._makeRequest("PUT", path, data, customHeaders);
    }

    delete(path, data = null, customHeaders = {}) {
        return this._makeRequest("DELETE", path, data, customHeaders);
    }

    _makeRequest(method, path, data, customHeaders) {
        const options = {
            method,
            headers: this._buildHeaders(customHeaders),
        };

        if (data && method !== "GET") {
            options.body = JSON.stringify(data);
        }

        return this._request(path, options);
    }

    _buildHeaders(customHeaders = {}) {
        const defaultHeaders = {
            Accept: "application/json",
            "Content-Type": "application/json",
        };

        // Agregar token de autorización si existe
        const token = this._getAuthToken();
        if (token) {
            defaultHeaders.Authorization = `Bearer ${token}`;
        }

        // Merge headers: custom headers override default ones
        return { ...defaultHeaders, ...customHeaders };
    }

    _getAuthToken() {
        try {
            return localStorage.getItem("token");
        } catch (error) {
            console.warn("No se pudo acceder al localStorage:", error);
            return null;
        }
    }

    async _request(path, options) {
        try {
            const url = `${this.baseURL}${path}`;
            const response = await fetch(url, options);

            // Verificar si la respuesta es exitosa
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Verificar si la respuesta tiene contenido JSON
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.includes("application/json")) {
                return await response.json();
            }

            return await response.text();
        } catch (error) {
            console.error("Request error:", error);
            throw error;
        }
    }
}

export const requestService = new Request();
