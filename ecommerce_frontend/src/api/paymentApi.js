import api from "./axios";

export async function initiateStripePayment(orderId) {

    const response = await api.post(
        "/payments/initiate/",
        {
            order_id: orderId,
            provider: "STRIPE",
        }
    );

    return response.data;
}