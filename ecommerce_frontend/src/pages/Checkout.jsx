import { useState } from "react";

import { Elements } from "@stripe/react-stripe-js";

import { stripePromise } from "../lib/stripe";

import { initiateStripePayment } from "../api/paymentApi";

import StripeCheckoutForm from "../components/StripeCheckoutForm";

export default function Checkout() {

    const [clientSecret, setClientSecret] = useState("");

    const [payment, setPayment] = useState(null);

    async function handlePayment() {

        try {

            const response =
                await initiateStripePayment(1);

            setPayment(response.payment);

            setClientSecret(
                response.client_secret
            );

        } catch (error) {

            console.error(error);

            alert("Payment initiation failed.");
            console.log(error.response);

            console.log(error.response.data);
        
            console.log(error.response.status);

        }

    }

    if (!clientSecret) {

        return (

            <div>

                <h2>Stripe Checkout</h2>

                <button onClick={handlePayment}>
                    Pay Now
                </button>

            </div>

        );

    }

    return (

        <Elements
            stripe={stripePromise}
            options={{
                clientSecret,
            }}
        >

            <StripeCheckoutForm
                payment={payment}
            />

        </Elements>

    );

}