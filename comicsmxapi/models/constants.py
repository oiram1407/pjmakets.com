class constants:
    #Varible for use everything
    Statuses = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    ]

    Statuses_orders = {
        ('pendding', "Pendding to pay"),
        ('paid', 'Paid'),
        ('shipping', 'Shipping'),
        ('delivery', "Delivery"),
        ('failed', "Failed"),
        ('completed', "Completed")
    }

    Statuses_notifications = [
        ('sent', 'Sent'),
        ('pedding', 'Pendding'),
        ('failed_to_send', 'Failed to send')
    ]

    Plataforms = [
        ("manually", "Manually"),
        ("mercado_libre", "Mercado Libre"),
        ("woocommerce", "WooCommerce"),
    ]

    ActionInventyory = [
        ("increment", "Increment"),
        ("decrement", "Decrement"),
    ]