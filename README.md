# Gold Transactions API

This is an API that allows users to manage gold transactions, including buying and selling gold, and checking the wallet balance. The API is built using Django and provides the following endpoints:

## Endpoints

### 1. **Buy Gold**
This endpoint allows authenticated users to buy gold by providing the amount in Rial.

- **URL**: `/transactions/buy/`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "amount_rial": "Amount in Rial"
    }
    ```
- **Response**:
    - **Success** (`201 Created`):
    ```json
    {
        "id": "Transaction ID",
        "user": "User ID",
        "amount_rial": "Amount in Rial",
        "gold_weight_gram": "Gold weight in grams",
        "price_per_gram": "Price per gram of gold",
        "status": "Transaction Status"
    }
    ```
    - **Error** (`400 Bad Request`):
    ```json
    {
        "error": "Insufficient wallet balance to make this purchase."
    }
    ```

#### **How it works**:
- The user sends a request with the `amount_rial`, which is the amount of money they want to spend to buy gold.
- The system checks if the user has enough balance in their wallet.
- If the balance is sufficient, the transaction is created, the wallet is updated with the new gold balance, and the user's Rial balance is reduced.

### 2. **Sell Gold**
This endpoint allows authenticated users to sell gold, which will update the user's wallet with the corresponding Rial.

- **URL**: `/transactions/sell/`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "gold_weight_gram": "Weight of gold in grams"
    }
    ```
- **Response**:
    - **Success** (`201 Created`):
    ```json
    {
        "id": "Transaction ID",
        "user": "User ID",
        "amount_rial": "Amount in Rial",
        "gold_weight_gram": "Gold weight in grams",
        "price_per_gram": "Price per gram of gold",
        "status": "Transaction Status"
    }
    ```
    - **Error** (`400 Bad Request`):
    ```json
    {
        "error": "Insufficient gold balance in wallet to complete the sale."
    }
    ```

#### **How it works**:
- The user sends a request with the `gold_weight_gram`, which is the weight of the gold they want to sell.
- The system checks if the user has enough gold in their wallet.
- If the balance is sufficient, the transaction is created, and the wallet is updated with the new Rial balance.



## Authentication

This API uses JWT authentication. Please include the token in the `Authorization` header when making requests.

- **Authorization Header**:
    ```
    Authorization: Bearer <your-jwt-token>
    ```

## Requirements

- Python 3.8+
- Django 4.x+
- djangorestframework
- djoser
- PyJWT

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/MotahareFallah/Gold_transactions.git
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run migrations to set up the database:
    ```bash
    python manage.py migrate
    ```

4. Create a superuser to access the Django admin:
    ```bash
    python manage.py createsuperuser
    ```

5. Start the development server:
    ```bash
    python manage.py runserver
    ```
