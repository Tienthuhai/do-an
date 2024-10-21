import tkinter as tk
from tkinter import messagebox, simpledialog
import csv
import os

# Class cha User
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# Class con Admin kế thừa từ User
class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)

# Class con Customer kế thừa từ User
class Customer(User):
    def __init__(self, username, password):
        super().__init__(username, password)

# Class xử lý lưu trữ dữ liệu
class DataManager:
    def __init__(self, users_file, menu_file):
        self.users_file = users_file
        self.menu_file = menu_file
        self.users = self.load_users()
        self.menu_items = self.load_menu()

    def load_users(self):
        users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["role"] == "admin":
                        users[row["username"]] = Admin(row["username"], row["password"])
                    else:
                        users[row["username"]] = Customer(row["username"], row["password"])
        return users

    def load_menu(self):
        menu_items = []
        if os.path.exists(self.menu_file):
            with open(self.menu_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    menu_items.append(row)
        return menu_items

    def save_user(self, username, password, role):
        with open(self.users_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password, role])
        if role == "admin":
            self.users[username] = Admin(username, password)
        else:
            self.users[username] = Customer(username, password)

    def save_food(self, food_name, price):
        with open(self.menu_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([food_name, price])
        self.menu_items.append([food_name, price])

    def delete_food(self, food_name):
        self.menu_items = [item for item in self.menu_items if item[0] != food_name]
        with open(self.menu_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.menu_items)

# Class xử lý đăng nhập
class LoginScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.username_entry = None
        self.password_entry = None
        self.setup()

    def setup(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Tên người dùng:").pack(pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)
        
        tk.Label(self.root, text="Mật khẩu:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(self.root, text="Đăng nhập", command=self.login).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        user = self.app.data_manager.users.get(username)
        if user and user.password == password:
            self.app.current_user = user
            messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
            if isinstance(user, Admin):
                self.app.show_admin_screen()
            else:
                self.app.show_customer_screen()
        else:
            messagebox.showerror("Lỗi", "Tên người dùng hoặc mật khẩu không chính xác!")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Class xử lý giao diện chức năng khách hàng
class CustomerScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup()

    def setup(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Chức năng Khách hàng", font=("Arial", 14, "bold")).pack(pady=10)
        functions_khach_hang = [
            "Đặt bàn và gọi món", "Đổi điểm tích lũy", 
            "Quản lý thông tin cá nhân", "Xem lịch sử hóa đơn"
        ]
        for func in functions_khach_hang:
            tk.Button(self.root, text=func, width=30, command=lambda f=func: self.show_message(f)).pack(pady=5)
        
        tk.Button(self.root, text="Đăng xuất", command=self.app.show_login_screen, fg="red").pack(pady=20)

    def show_message(self, function_name):
        messagebox.showinfo("Thông báo", f"Chức năng '{function_name}' đang được phát triển")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Class xử lý giao diện chức năng Admin
class AdminScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup()

    def setup(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Chức năng Admin", font=("Arial", 14, "bold")).pack(pady=10)
        functions_nhan_vien = [
            "Quản lý Bàn", "Quản lý Nguyên Liệu",
            "Quản lý Thực Đơn", "Quản lý Nhân Sự", 
            "Thống kê Hóa Đơn", "Quản lý khách hàng",
            "Thêm tài khoản"
        ]
        for func in functions_nhan_vien:
            if func == "Quản lý Thực Đơn":
                tk.Button(self.root, text=func, width=30, command=self.app.show_menu_screen).pack(pady=5)
            elif func == "Thêm tài khoản":
                tk.Button(self.root, text=func, width=30, command=self.app.show_add_user_screen).pack(pady=5)
            elif func == "Quản lý Nhân Sự":
                tk.Button(self.root, text=func, width=30, command=self.app.show_employee_screen).pack(pady=5)
            else:
                tk.Button(self.root, text=func, width=30, command=lambda f=func: self.show_message(f)).pack(pady=5)

        tk.Button(self.root, text="Đăng xuất", command=self.app.show_login_screen, fg="red").pack(pady=20)

    def show_message(self, function_name):
        messagebox.showinfo("Thông báo", f"Chức năng '{function_name}' đang được phát triển")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Class xử lý thêm tài khoản
class AddUserScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup()

    def setup(self):
        self.clear_screen()

        tk.Label(self.root, text="Thêm Tài Khoản Mới", font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(self.root, text="Tên người dùng:").pack(pady=10)
        self.new_username_entry = tk.Entry(self.root)
        self.new_username_entry.pack(pady=5)
        
        tk.Label(self.root, text="Mật khẩu:").pack(pady=10)
        self.new_password_entry = tk.Entry(self.root, show="*")
        self.new_password_entry.pack(pady=5)
        
        tk.Label(self.root, text="Vai trò (admin/customer):").pack(pady=10)
        self.new_role_entry = tk.Entry(self.root)
        self.new_role_entry.pack(pady=5)
        
        tk.Button(self.root, text="Thêm Tài Khoản", command=self.add_user).pack(pady=20)
        tk.Button(self.root, text="Quay lại", command=self.app.show_admin_screen, fg="red").pack(pady=5)

    def add_user(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        role = self.new_role_entry.get()
        
        if username and password and role in ["admin", "customer"]:
            if username not in self.app.data_manager.users:
                self.app.data_manager.save_user(username, password, role)
                messagebox.showinfo("Thông báo", "Thêm tài khoản thành công!")
                self.app.show_admin_screen()
            else:
                messagebox.showerror("Lỗi", "Tài khoản đã tồn tại!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin và chọn vai trò hợp lệ!")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Class xử lý quản lý nhân sự
class EmployeeScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup()

    def setup(self):
        self.clear_screen()

        tk.Label(self.root, text="Quản lý Nhân sự", font=("Arial", 14, "bold")).pack(pady=10)

        # Tạo Listbox để hiển thị danh sách nhân viên
        self.employee_listbox = tk.Listbox(self.root, width=50, height=10)
        self.employee_listbox.pack(pady=10)

        # Nút để thực hiện các thao tác quản lý nhân sự
        tk.Button(self.root, text="Xem Danh Sách Nhân Viên", command=self.show_employees).pack(pady=5)
        tk.Button(self.root, text="Thêm Nhân Viên", command=self.add_employee).pack(pady=5)
        tk.Button(self.root, text="Sửa Nhân Viên", command=self.edit_employee).pack(pady=5)
        tk.Button(self.root, text="Xóa Nhân Viên", command=self.delete_employee).pack(pady=5)
        tk.Button(self.root, text="Quay lại", command=self.app.show_admin_screen).pack(pady=5)

        self.update_employee_listbox()

    def update_employee_listbox(self):
        """Cập nhật nội dung của Listbox từ file danh sách nhân viên."""
        self.employee_listbox.delete(0, tk.END)
        try:
            with open("employees.csv", mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 3:
                        self.employee_listbox.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]}")
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file danh sách nhân viên!")

    def show_employees(self):
        """Hiển thị danh sách nhân viên trong Listbox."""
        self.update_employee_listbox()

    def add_employee(self):
        name = simpledialog.askstring("Thêm Nhân Viên", "Nhập tên nhân viên:")
        position = simpledialog.askstring("Thêm Nhân Viên", "Nhập chức vụ:")
        salary = simpledialog.askstring("Thêm Nhân Viên", "Nhập mức lương:")
        
        if name and position and salary:
            with open("employees.csv", mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([name, position, salary])
            messagebox.showinfo("Thông báo", f"Nhân viên {name} đã được thêm!")
            self.update_employee_listbox()
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

    def edit_employee(self):
        selected_item = self.employee_listbox.curselection()
        if selected_item:
            name = self.employee_listbox.get(selected_item[0]).split(" | ")[0]
            new_position = simpledialog.askstring("Sửa Nhân Viên", "Nhập chức vụ mới:")
            new_salary = simpledialog.askstring("Sửa Nhân Viên", "Nhập mức lương mới:")
            if new_position and new_salary:
                employee_data = []
                found = False

                with open("employees.csv", mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 3:
                            if row[0] == name:
                                found = True
                                employee_data.append([name, new_position, new_salary])
                            else:
                                employee_data.append(row)

                if found:
                    with open("employees.csv", mode='w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerows(employee_data)
                    messagebox.showinfo("Thông báo", f"Nhân viên {name} đã được sửa!")
                    self.update_employee_listbox()
                else:
                    messagebox.showerror("Lỗi", f"Nhân viên '{name}' không tồn tại!")
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhân viên để sửa!")

    def delete_employee(self):
        selected_item = self.employee_listbox.curselection()
        if selected_item:
            name = self.employee_listbox.get(selected_item[0]).split(" | ")[0]
            employee_data = []
            found = False

            with open("employees.csv", mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 3:
                        if row[0] != name:
                            employee_data.append(row)
                        else:
                            found = True

            if found:
                with open("employees.csv", mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(employee_data)
                messagebox.showinfo("Thông báo", f"Nhân viên {name} đã được xóa!")
                self.update_employee_listbox()
            else:
                messagebox.showerror("Lỗi", f"Nhân viên '{name}' không tồn tại!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhân viên để xóa!")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
class MenuScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup()

    def setup(self):
        self.clear_screen()

        tk.Label(self.root, text="Quản lý Thực đơn", font=("Arial", 14, "bold")).pack(pady=10)

        # Tạo Listbox để hiển thị thực đơn
        self.menu_listbox = tk.Listbox(self.root, width=50, height=10)
        self.menu_listbox.pack(pady=10)

        # Nút để hiển thị thực đơn
        tk.Button(self.root, text="Xem Thực Đơn", command=self.show_menu).pack(pady=5)
        tk.Button(self.root, text="Thêm món ăn", command=self.add_food).pack(pady=5)
        tk.Button(self.root, text="Sửa món ăn", command=self.edit_food).pack(pady=5)
        tk.Button(self.root, text="Xóa món ăn", command=self.delete_food).pack(pady=5)
        tk.Button(self.root, text="Quay lại", command=self.app.show_admin_screen).pack(pady=5)

        # Gọi phương thức để cập nhật Listbox khi khởi tạo
        self.update_menu_listbox()

    def update_menu_listbox(self):
        """Cập nhật nội dung của Listbox từ file thực đơn."""
        self.menu_listbox.delete(0, tk.END)  # Xóa nội dung cũ
        try:
            with open("menu.csv", mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 3:  # Kiểm tra xem có đủ cột không
                        # Thêm món ăn vào Listbox
                        self.menu_listbox.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]}")
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file thực đơn!")

    def show_menu(self):
        """Hiển thị thực đơn trong Listbox."""
        self.update_menu_listbox()  # Cập nhật nội dung Listbox mỗi khi người dùng nhấn nút

    def add_food(self):
        food_name = simpledialog.askstring("Thêm Món Ăn", "Nhập tên món ăn:")
        ingredients = simpledialog.askstring("Thêm Món Ăn", "Nhập nguyên liệu:")
        price = simpledialog.askstring("Thêm Món Ăn", "Nhập giá:")
        
        if food_name and ingredients and price:
            with open("menu.csv", mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([food_name, ingredients, price])
            messagebox.showinfo("Thông báo", f"Món {food_name} đã được thêm!")
            self.update_menu_listbox()  # Cập nhật lại Listbox sau khi thêm món
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

    def edit_food(self):
        selected_item = self.menu_listbox.curselection()
        if selected_item:
            food_name = self.menu_listbox.get(selected_item[0]).split(" | ")[0]  # Lấy tên món ăn đã chọn
            
            new_ingredients = simpledialog.askstring("Sửa Món Ăn", "Nhập nguyên liệu mới:")
            new_price = simpledialog.askstring("Sửa Món Ăn", "Nhập giá mới:")
            if new_ingredients and new_price:
                menu_items = []
                found = False

                # Đọc dữ liệu từ file
                with open("menu.csv", mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 3:
                            if row[0] == food_name:
                                found = True
                                menu_items.append([food_name, new_ingredients, new_price])
                            else:
                                menu_items.append(row)

                # Ghi lại file nếu tìm thấy món ăn
                if found:
                    with open("menu.csv", mode='w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerows(menu_items)
                    messagebox.showinfo("Thông báo", f"Món {food_name} đã được sửa!")
                    self.update_menu_listbox()  # Cập nhật Listbox sau khi sửa món
                else:
                    messagebox.showerror("Lỗi", f"Món ăn '{food_name}' không tồn tại!")
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn món ăn để sửa!")

    def delete_food(self):
        selected_item = self.menu_listbox.curselection()
        if selected_item:
            food_name = self.menu_listbox.get(selected_item[0]).split(" | ")[0]  # Lấy tên món ăn đã chọn
            
            menu_items = []
            found = False

            # Đọc dữ liệu từ file
            with open("menu.csv", mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 3:
                        if row[0] != food_name:
                            menu_items.append(row)
                        else:
                            found = True

            # Ghi lại file nếu tìm thấy món ăn
            if found:
                with open("menu.csv", mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(menu_items)
                messagebox.showinfo("Thông báo", f"Món {food_name} đã được xóa!")
                self.update_menu_listbox()  # Cập nhật Listbox sau khi xóa món
            else:
                messagebox.showerror("Lỗi", f"Món ăn '{food_name}' không tồn tại!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn món ăn để xóa!")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Class quản lý ứng dụng
class RestaurantApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quản lý nhà hàng")
        self.data_manager = DataManager('users.csv', 'menu.csv')
        self.current_user = None
        self.root.geometry("400x400")
        
        self.login_screen = LoginScreen(self.root, self)
        self.admin_screen = AdminScreen(self.root, self)
        self.customer_screen = CustomerScreen(self.root, self)
        self.menu_screen = MenuScreen(self.root, self)
        self.employee_screen = EmployeeScreen(self.root, self)
        self.add_user_screen = AddUserScreen(self.root, self)

        self.show_login_screen()
        
        self.root.mainloop()

    def show_login_screen(self):
        self.login_screen.setup()

    def show_admin_screen(self):
        self.admin_screen.setup()

    def show_customer_screen(self):
        self.customer_screen.setup()

    def show_menu_screen(self):
        self.menu_screen.setup()

    def show_employee_screen(self):
        self.employee_screen.setup()

    def show_add_user_screen(self):
        self.add_user_screen.setup()

# Khởi động ứng dụng
if __name__ == "__main__":
    RestaurantApp()
