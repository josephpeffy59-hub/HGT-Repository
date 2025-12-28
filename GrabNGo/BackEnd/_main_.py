# --- ADD THIS CODE TO THE BOTTOM OF YOUR FILE ---

# 1. Initialize the adder class
db_adder = ADD_INTO_TABLES(con)

def populate_sample_data():
    print("Populating database with Cameroonian records...")

    # --- 1. ADD 10 UNIQUE BUYERS ---
    # (name, e_mail, location, phone, password, date_of_creation)
    buyers = [
        ("Ngo Batoum Marie", "marie.bat@camnet.cm", "Akwa, Douala", 699123456, "Pass1!", "2024-01-10"),
        ("Tanyi Kevin Ashu", "kevin.ashu@gmail.com", "Molyko, Buea", 677889900, "Pass2!", "2024-01-11"),
        ("Amadou Bello", "amadou.b@yahoo.fr", "Garoua", 691223344, "Pass3!", "2024-01-12"),
        ("Abena Faustin", "faustin.abena@gmail.com", "Bastos, Yaoundé", 655443322, "Pass4!", "2024-01-13"),
        ("Bih Mirabelle", "mirabelle.bih@outlook.com", "Bamenda Up-Station", 670112233, "Pass5!", "2024-01-14"),
        ("Ewane Serge", "ewane.serge@gmail.com", "Nkongsamba", 694556677, "Pass6!", "2024-01-15"),
        ("Sali Hamadou", "sali.h@maroua.it", "Maroua", 651998877, "Pass7!", "2024-01-16"),
        ("Grace Enow", "grace.enow@gmail.com", "Limbe Down-Beach", 671221122, "Pass8!", "2024-01-17"),
        ("Fodjo Guy", "guy.fodjo@gmail.com", "Bafoussam", 696000111, "Pass9!", "2024-01-18"),
        ("Zra Dieudonne", "zra.d@gmail.com", "Mora", 650445566, "Pass10!", "2024-01-19")
    ]
    for b in buyers:
        db_adder.add_into_buyer_account(*b)

    # --- 2. ADD 10 UNIQUE SELLERS ---
    # (name, buisness_name, buisness_type, phone, e_mail, password, location, open_time, rating, sales, date)
    sellers = [
        ("Fosso Kamga", "Fosso Wholesale", "Food & Beverage", 677978500, "fosso@gmail.com", "SPass1", "Marché Central, Yaoundé", "08:00", 4.5, 120, "2023-10-01"),
        ("Mama Chantal", "Chantal's Kitchen", "Restaurant", 699001122, "chantal@yahoo.com", "SPass2", "Bonapriso, Douala", "07:00", 4.8, 550, "2023-11-05"),
        ("Tchakounte Paul", "Paulin Tech", "Electronics", 678223344, "paul.tech@gmail.com", "SPass3", "Avenue Kennedy, Yaoundé", "09:00", 3.9, 85, "2023-12-10"),
        ("Musa Isa", "Sahel Fabrics", "Clothing", 655112233, "musa.isa@gmail.com", "SPass4", "Ngaoundéré", "08:30", 4.2, 210, "2024-01-02"),
        ("Brenda Bi", "B-Beauty", "Cosmetics", 670445566, "brenda.bi@gmail.com", "SPass5", "Commercial Ave, Bamenda", "08:00", 4.7, 340, "2024-01-15"),
        ("Etoundi Jean", "Etoundi Agri", "Agriculture", 691778899, "etoundi@gmail.com", "SPass6", "Mbalmayo", "06:00", 4.4, 95, "2024-02-01"),
        ("Njoh Samuel", "Sams Furniture", "Carpentry", 675334455, "sam.njoh@gmail.com", "SPass7", "Deido, Douala", "08:00", 4.0, 45, "2024-02-10"),
        ("Amina Dada", "Amina Spices", "Groceries", 651119900, "amina.d@gmail.com", "SPass8", "Kousseri", "07:30", 4.6, 600, "2024-02-15"),
        ("Che Kevin", "Che Auto Parts", "Automotive", 674221133, "che.auto@gmail.com", "SPass9", "Molyko, Buea", "08:00", 3.5, 120, "2024-02-20"),
        ("Nguemo Pierre", "Pierre Stationery", "Office Supply", 693223344, "pierre@gmail.com", "SPass10", "Dschang", "07:00", 4.1, 80, "2024-02-25")
    ]
    for s in sellers:
        db_adder.add_into_seller_account(*s)

    # --- 3. ADD 10 UNIQUE PRODUCTS ---
    # (name, qty)
    products = [
        ("Penja Pepper (500g)", 150), ("Ndole Leaves (Bag)", 200), ("Rice 25kg Neima", 80),
        ("Smartphone Camon 20", 30), ("African Print Wax", 100), ("Organic Cocoa Butter", 60),
        ("Plantain (Large Bunch)", 300), ("Table Water 1.5L x6", 500), ("Palm Oil 5L", 120),
        ("Office Paper A4", 400)
    ]
    for p in products:
        db_adder.add_into_product(*p)

    # --- 4. SELLER_PRODUCT (Establishing One-to-Many Relationships) ---
    # Seller 1 (Fosso) has 3 products
    db_adder.add_into_SellerProduct(1, 1, "Authentic Penja Pepper", "Spices", 4500, 50, "img/penja.jpg")
    db_adder.add_into_SellerProduct(1, 3, "High quality parboiled rice", "Grains", 13500, 20, "img/rice.jpg")
    db_adder.add_into_SellerProduct(1, 9, "Pure red palm oil", "Oil", 3500, 40, "img/oil.jpg")

    # Seller 3 (Tchakounte) has 2 products
    db_adder.add_into_SellerProduct(3, 4, "Brand new Tecno smartphone", "Tech", 125000, 10, "img/phone.jpg")
    db_adder.add_into_SellerProduct(3, 10, "Box of 5 reams", "Stationery", 18000, 15, "img/paper.jpg")

    # Filling remaining 5 fields to reach 10 total entries in this table
    db_adder.add_into_SellerProduct(2, 7, "Fresh from Mbalmayo", "Food", 2500, 100, "img/plantain.jpg")
    db_adder.add_into_SellerProduct(4, 5, "Super Wax 6 yards", "Fashion", 12000, 50, "img/wax.jpg")
    db_adder.add_into_SellerProduct(5, 6, "Natural Skin Care", "Beauty", 3000, 30, "img/cocoa.jpg")
    db_adder.add_into_SellerProduct(8, 2, "Freshly washed ndole", "Food", 1000, 50, "img/ndole.jpg")
    db_adder.add_into_SellerProduct(10, 10, "Single ream", "Stationery", 3800, 100, "img/paper2.jpg")

    # --- 5. ORDERS (10 records) ---
    # (Product_ID, Seller_ID, Buyer_ID, price, qty, total)
    for i in range(1, 11):
        # Using simple increment to ensure foreign keys 1-10 are met
        db_adder.add_into_Orders(i, i, i, 5000, 2, 10000)

    # --- 6. HISTORY (10 records) ---
    # (Buyer_ID, Seller_ID, Product_ID, qty, price, date)
    for i in range(1, 11):
        db_adder.add_into_History(i, i, i, 1, 5000, "2024-03-01")

    print("Populating complete. 10 fields added to each table.")

# Execute the function
populate_sample_data()



import sqlite3

# Note: Ensure your Database_Manipulation classes handle con.commit() 
# or call con.commit() after these methods.

class Seller_Store_Manager:
    def __init__(self, con, name):
        self.con = con # Store connection to commit changes
        self.getter = Get_From_Tables(con)
        self.displayer = Display_From_Table(con)
        self.seller_name = name
        self.seller_id = self.getter.get_seller_id_by_name(name)
        self.adder = ADD_INTO_TABLES(con)
        self.updater = Update_Table(con)
        self.deleter = Delete_From_Table(con)

    # --- Financial Logic ---


    def open_store(self):
        # Added 'self.' to seller_id
        self.updater.update_seller_status(self.seller_id, "Open")
        self.con.commit()
        print("Store is now Open")

    def close_store(self):
        # Added 'self.' to seller_id
        self.updater.update_seller_status(self.seller_id, "Closed")
        self.con.commit()
        print("Store is now Closed")