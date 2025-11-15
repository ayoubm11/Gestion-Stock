import os
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from models import Item
from db import DatabaseManager


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des stocks")
        self.root.geometry("1000x640")
        self.db = DatabaseManager()

        self.logo_pil = None
        self.logo_img = None
        self.logo_scale = 1.0
        self.logo_growing = True
        # configurable animation parameters
        self.logo_speed = 0.014
        self.logo_min_scale = 0.94
        self.logo_max_scale = 1.14
        self.header_pulse_interval = 700

        self._build_ui()
        self._refresh_list()

    def _build_ui(self):
        # Header bar (logo left, search center)
        self.header = ctk.CTkFrame(self.root, height=64, fg_color=("#f0f4f7", "#1f2b36"))
        self.header.pack(fill="x", side="top")

        # Left: logo (try .ico first, then .png)
        logo_ico_path = "logo.ico"
        logo_png_path = "logo.png"
        logo_path = None
        
        if os.path.exists(logo_ico_path):
            logo_path = logo_ico_path
        elif os.path.exists(logo_png_path):
            logo_path = logo_png_path
        
        if logo_path:
            try:
                self.logo_pil = Image.open(logo_path).convert("RGBA")
                # Set window icon (use original for .ico)
                if logo_path.endswith(".ico"):
                    try:
                        self.root.iconbitmap(logo_path)
                    except Exception:
                        pass
                # Resize for header display
                img = self.logo_pil.resize((52, 52), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                self.logo_lbl = ctk.CTkLabel(self.header, image=self.logo_img, text="")
            except Exception:
                self.logo_lbl = ctk.CTkLabel(self.header, text="LOGO")
        else:
            self.logo_lbl = ctk.CTkLabel(self.header, text="LOGO", width=100)
        self.logo_lbl.pack(side="left", padx=12, pady=6)

        # Center: search bar
        center_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        center_frame.pack(side="left", expand=True)
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(center_frame, width=480, placeholder_text="Recherche...")
        self.search_entry.pack(padx=10, pady=10, side="left")
        self.search_entry.configure(textvariable=self.search_var)
        self.search_entry.bind("<FocusIn>", lambda e: self._animate_search_expand(True))
        self.search_entry.bind("<FocusOut>", lambda e: self._animate_search_expand(False))
        search_btn = ctk.CTkButton(center_frame, text="Chercher", command=self.search, width=90)
        search_btn.pack(padx=6, pady=10, side="left")

        # Main content: left for input (two columns inside), right for display
        content = ctk.CTkFrame(self.root)
        content.pack(fill="both", expand=True, padx=12, pady=12)

        left_frame = ctk.CTkFrame(content, width=360)
        left_frame.pack(side="left", fill="y", padx=(0, 12))

        # Input fields (two-column look using grid)
        lbl_name = ctk.CTkLabel(left_frame, text="Nom")
        lbl_name.grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.name_var = ctk.StringVar()
        ent_name = ctk.CTkEntry(left_frame, textvariable=self.name_var)
        ent_name.grid(row=0, column=1, padx=8, pady=6)

        lbl_desc = ctk.CTkLabel(left_frame, text="Description")
        lbl_desc.grid(row=1, column=0, sticky="w", padx=8, pady=6)
        self.desc_var = ctk.StringVar()
        ent_desc = ctk.CTkEntry(left_frame, textvariable=self.desc_var)
        ent_desc.grid(row=1, column=1, padx=8, pady=6)

        lbl_qty = ctk.CTkLabel(left_frame, text="Quantité")
        lbl_qty.grid(row=2, column=0, sticky="w", padx=8, pady=6)
        self.qty_var = ctk.IntVar(value=0)
        ent_qty = ctk.CTkEntry(left_frame, textvariable=self.qty_var)
        ent_qty.grid(row=2, column=1, padx=8, pady=6)

        lbl_price = ctk.CTkLabel(left_frame, text="Prix")
        lbl_price.grid(row=3, column=0, sticky="w", padx=8, pady=6)
        self.price_var = ctk.DoubleVar(value=0.0)
        ent_price = ctk.CTkEntry(left_frame, textvariable=self.price_var)
        ent_price.grid(row=3, column=1, padx=8, pady=6)

        btn_add = ctk.CTkButton(left_frame, text="Ajouter", command=self.add_item)
        btn_add.grid(row=4, column=0, columnspan=2, sticky="ew", padx=8, pady=6)

        btn_update = ctk.CTkButton(left_frame, text="Mettre à jour", command=self.update_item)
        btn_update.grid(row=5, column=0, columnspan=2, sticky="ew", padx=8, pady=6)

        btn_delete = ctk.CTkButton(left_frame, text="Supprimer", command=self.delete_item)
        btn_delete.grid(row=6, column=0, columnspan=2, sticky="ew", padx=8, pady=6)

        btn_export = ctk.CTkButton(left_frame, text="Exporter Excel", command=self.export_excel)
        btn_export.grid(row=7, column=0, columnspan=2, sticky="ew", padx=8, pady=6)

        btn_import_csv = ctk.CTkButton(left_frame, text="Importer CSV", command=self.import_csv)
        btn_import_csv.grid(row=8, column=0, columnspan=2, sticky="ew", padx=8, pady=6)

        btn_export_csv = ctk.CTkButton(left_frame, text="Exporter CSV", command=self.export_csv)
        btn_export_csv.grid(row=9, column=0, columnspan=2, sticky="ew", padx=8, pady=6)

        # Right: display (slightly reduced width compared to before)
        right_frame = ctk.CTkFrame(content)
        right_frame.pack(side="left", fill="both", expand=True)

        self.tree = ttk.Treeview(right_frame, columns=("name", "description", "qty", "price"), show="headings")
        self.tree.heading("name", text="Nom")
        self.tree.heading("description", text="Description")
        self.tree.heading("qty", text="Quantité")
        self.tree.heading("price", text="Prix")
        self.tree.column("description", width=300)
        self.tree.pack(fill="both", expand=True, side="left")

        sb = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        sb.pack(side="left", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        # hover highlight support
        self.tree.tag_configure('hover', background="#e8f4ff")
        self._hover_row = None
        self.tree.bind("<Motion>", self._on_tree_motion)
        self.tree.bind("<Leave>", self._on_tree_leave)

    def _refresh_list(self, items=None):
        for r in self.tree.get_children():
            self.tree.delete(r)
        if items is None:
            items = self.db.get_all_items()
        for it in items:
            self.tree.insert("", "end", iid=str(it.id), values=(it.name, it.description, it.quantity, it.price))

    def add_item(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Validation", "Nom requis")
            return
        item = Item(id=None, name=name, description=self.desc_var.get().strip(), quantity=int(self.qty_var.get()), price=float(self.price_var.get()))
        self.db.add_item(item)
        self._refresh_list()

    def update_item(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Sélectionnez un article")
            return
        item_id = int(sel[0])
        item = Item(id=item_id, name=self.name_var.get().strip(), description=self.desc_var.get().strip(), quantity=int(self.qty_var.get()), price=float(self.price_var.get()))
        ok = self.db.update_item(item)
        if ok:
            self._refresh_list()
        else:
            messagebox.showerror("Erreur", "Mise à jour échouée")

    def delete_item(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Sélectionnez un article")
            return
        item_id = int(sel[0])
        if messagebox.askyesno("Confirmer", "Supprimer cet article ?"):
            ok = self.db.delete_item(item_id)
            if ok:
                self._refresh_list()

    def on_select(self, _ev):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        vals = self.tree.item(iid, "values")
        # vals = (name, description, qty, price)
        self.name_var.set(vals[0])
        self.desc_var.set(vals[1])
        try:
            self.qty_var.set(int(vals[2]))
        except Exception:
            self.qty_var.set(0)
        try:
            self.price_var.set(float(vals[3]))
        except Exception:
            self.price_var.set(0.0)

    def search(self):
        term = self.search_var.get().strip()
        if not term:
            self._refresh_list()
            return
        res = self.db.search_items(term)
        self._refresh_list(res)

    def export_excel(self):
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not path:
            return
        try:
            self.db.export_excel(path)
            messagebox.showinfo("Export", f"Exporté vers {path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec export: {e}")

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            self.db.export_csv(path)
            messagebox.showinfo("Export", f"Exporté vers {path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec export CSV: {e}")

    def import_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            self.db.import_csv(path)
            self._refresh_list()
            messagebox.showinfo("Import", f"Import terminé depuis {path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec import CSV: {e}")

    def init_mysql_db(self):
        ok = self.db.create_database()
        if ok:
            messagebox.showinfo("MySQL", "Base créée (ou déjà existante)")
        else:
            messagebox.showerror("MySQL", "Impossible de créer la base - vérifiez la connexion et les identifiants dans config.json")

    def init_mysql_db(self):
        ok = self.db.create_database()
        if ok:
            messagebox.showinfo("MySQL", "Base créée (ou déjà existante)")
        else:
            messagebox.showerror("MySQL", "Impossible de créer la base - vérifiez la connexion et les identifiants dans config.json")

    # Hover handlers for treeview
    def _on_tree_motion(self, event):
        row_id = self.tree.identify_row(event.y)
        if row_id != getattr(self, '_hover_row', None):
            prev = getattr(self, '_hover_row', None)
            if prev:
                tags = list(self.tree.item(prev, 'tags'))
                if 'hover' in tags:
                    tags.remove('hover')
                    self.tree.item(prev, tags=tuple(tags))
            if row_id:
                tags = list(self.tree.item(row_id, 'tags'))
                if 'hover' not in tags:
                    tags.append('hover')
                    self.tree.item(row_id, tags=tuple(tags))
            self._hover_row = row_id

    def _on_tree_leave(self, _event):
        prev = getattr(self, '_hover_row', None)
        if prev:
            tags = list(self.tree.item(prev, 'tags'))
            if 'hover' in tags:
                tags.remove('hover')
                self.tree.item(prev, tags=tuple(tags))
        self._hover_row = None

    # --- Animations ---
    def _start_animations(self):
        pass

    def _animate_header_pulse(self):
        pass

    def _animate_logo(self):
        pass

    def _animate_search_expand(self, expand: bool):
        # animation disabled
        pass


if __name__ == "__main__":
    import os
    root = ctk.CTk()
    app = InventoryApp(root)
    root.mainloop()
