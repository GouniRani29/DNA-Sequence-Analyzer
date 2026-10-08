const API_URL = "http://localhost:8080/api/auth";

// =====================================================
// REGISTER
// =====================================================

export const registerUser = async (
    username,
    email,
    password
) => {

    const response = await fetch(
        `${API_URL}/register`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username,
                email,
                password
            })
        }
    );

    const data = await response.json();

    if (!response.ok || !data.success) {

        throw new Error(
            data.message || "Registration failed"
        );
    }

    return data;
};


// =====================================================
// LOGIN
// =====================================================

export const loginUser = async (
    username,
    password
) => {

    const response = await fetch(
        `${API_URL}/login`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username,
                password
            })
        }
    );

    const data = await response.json();

    if (!response.ok || !data.success) {

        throw new Error(
            data.message || "Login failed"
        );
    }

    return data;
};