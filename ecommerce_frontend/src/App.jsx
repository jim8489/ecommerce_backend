import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import Checkout from "./pages/Checkout";
import PaymentSuccess from "./pages/PaymentSuccess";

export default function App() {

  return (

      <BrowserRouter>

          <Routes>

              <Route
                  path="/"
                  element={<Checkout />}
              />

              <Route
                  path="/payment-success"
                  element={<PaymentSuccess />}
              />

          </Routes>

      </BrowserRouter>

  );

}