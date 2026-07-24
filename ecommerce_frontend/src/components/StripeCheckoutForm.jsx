import {
    PaymentElement,
    useElements,
    useStripe,
} from "@stripe/react-stripe-js";

export default function StripeCheckoutForm() {

    const stripe = useStripe();

    const elements = useElements();

    async function handleSubmit(e) {

        e.preventDefault();

        if (!stripe || !elements) {
            return;
        }

        const result =
            await stripe.confirmPayment({

                elements,

                confirmParams: {
                    return_url:
                        "http://localhost:5173/payment-success",
                },

                redirect: "if_required",
            });

        if (result.error) {

            alert(result.error.message);

            return;

        }

        alert("Payment Successful");

    }

    return (

        <form onSubmit={handleSubmit}>

            <PaymentElement />

            <button
                type="submit"
                disabled={!stripe}
            >
                Pay
            </button>

        </form>

    );

}