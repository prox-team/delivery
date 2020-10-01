db.CreateUser(
    {
      user: "delivery-user",
      pwd: "delivery-password",
      roles: [
          {
              role: "readWrite",
              db: "delivery-base"
          }
      ]
    }