from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('contact/', views.contact,name='contact'),
    path('login/', views.login,name='login'),
    path('register/', views.register,name='register'),
    path('logout/', views.logout,name='logout'),
    path('forgot_password/', views.forgot_password,name='forgot_password'),
    path('validate_otp/',views.validate_otp,name='validate_otp'),
    path('update_password/',views.update_password,name='update_password'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('change_password/',views.change_password,name='change_password'),
    path('my_account/',views.my_account,name='my_account'),
    path('seller_index/',views.seller_index,name='seller_index'),
    path('seller_register/',views.seller_register,name='seller_register'),
    path('seller_login/',views.seller_login,name='seller_login'),

    # Women Cloth URL
    path('add_women_cloths/',views.add_women_cloths,name='add_women_cloths'),
    path('view_top/',views.view_top,name='view_top'),
    path('view_pant/',views.view_pant,name='view_pant'),
    path('view_saree/',views.view_saree,name='view_saree'),
    path('view_punjabi/',views.view_punjabi,name='view_punjabi'),
    path('view_western/',views.view_western,name='view_western'),
    path('wc_product_detail/<int:pk>/',views.wc_product_detail,name='wc_product_detail'),
    path('wc_stock_avaibility/<int:pk>/',views.wc_stock_avaibility,name='wc_stock_avaibility'),
    path('wc_delete/<int:pk>/',views.wc_delete,name='wc_delete'),
    path('wc_edit/<int:pk>/',views.wc_edit,name='wc_edit'),

    # Men Cloth URL
    path('add_men_cloths/',views.add_men_cloths,name='add_men_cloths'),
    path('view_shirt/',views.view_shirt,name='view_shirt'),
    path('view_tshirt/',views.view_tshirt,name='view_tshirt'),
    path('view_jeans/',views.view_jeans,name='view_jeans'),
    path('view_jackets/',views.view_jackets,name='view_jackets'),
    path('view_casual/',views.view_casual,name='view_casual'),
    path('mc_product_detail/<int:pk>/',views.mc_product_detail,name='mc_product_detail'),
    path('mc_stock_avaibility/<int:pk>/',views.mc_stock_avaibility,name='mc_stock_avaibility'),
    path('mc_delete/<int:pk>/',views.mc_delete,name='mc_delete'),
    path('mc_edit/<int:pk>/',views.mc_edit,name='mc_edit'),

    # Women Accessories URL
    path('add_women_acc/',views.add_women_acc,name='add_women_acc'),
    path('view_sunglasses/',views.view_sunglasses,name='view_sunglasses'),
    path('view_necklace/',views.view_necklace,name='view_necklace'),
    path('view_watch/',views.view_watch,name='view_watch'),
    path('view_tie/',views.view_tie,name='view_tie'),
    path('view_purse/',views.view_purse,name='view_purse'),
    path('view_ring/',views.view_ring,name='view_ring'),
    path('view_hairband/',views.view_hairband,name='view_hairband'),
    path('view_cap/',views.view_cap,name='view_cap'),
    path('wa_product_detail/<int:pk>/',views.wa_product_detail,name='wa_product_detail'),
    path('wa_stock_avaibility/<int:pk>/',views.wa_stock_avaibility,name='wa_stock_avaibility'),
    path('wa_delete/<int:pk>/',views.wa_delete,name='wa_delete'),
    path('wa_edit/<int:pk>/',views.wa_edit,name='wa_edit'),

    # Men Accessories URL
    path('add_men_acc/',views.add_men_acc,name='add_men_acc'),
    path('view_m_sunglasses/',views.view_m_sunglasses,name='view_m_sunglasses'),
    path('view_suspenders/',views.view_suspenders,name='view_suspenders'),
    path('view_m_watch/',views.view_m_watch,name='view_m_watch'),
    path('view_m_tie/',views.view_m_tie,name='view_m_tie'),
    path('view_m_purse/',views.view_m_purse,name='view_m_purse'),
    path('view_belt/',views.view_belt,name='view_belt'),
    path('view_socks/',views.view_socks,name='view_socks'),
    path('view_m_cap/',views.view_m_cap,name='view_m_cap'),
    path('ma_product_detail/<int:pk>/',views.ma_product_detail,name='ma_product_detail'),
    path('ma_stock_avaibility/<int:pk>/',views.ma_stock_avaibility,name='ma_stock_avaibility'),
    path('ma_delete/<int:pk>/',views.ma_delete,name='ma_delete'),
    path('ma_edit/<int:pk>/',views.ma_edit,name='ma_edit'),

    # Women Footwear URL
    path('add_women_footwear/',views.add_women_footwear,name='add_women_footwear'),
    path('view_wedges/',views.view_wedges,name='view_wedges'),
    path('view_ballerinas/',views.view_ballerinas,name='view_ballerinas'),
    path('view_canvas_shoes/',views.view_canvas_shoes,name='view_canvas_shoes'),
    path('view_wellington_boots/',views.view_wellington_boots,name='view_wellington_boots'),
    path('view_flip_flop/',views.view_flip_flop,name='view_flip_flop'),
    path('view_sandals/',views.view_sandals,name='view_sandals'),
    path('view_sport_shoes/',views.view_sport_shoes,name='view_sport_shoes'),
    path('view_heels/',views.view_heels,name='view_heels'),
    path('wf_product_detail/<int:pk>/',views.wf_product_detail,name='wf_product_detail'),
    path('wf_stock_avaibility/<int:pk>/',views.wf_stock_avaibility,name='wf_stock_avaibility'),
    path('wf_delete/<int:pk>/',views.wf_delete,name='wf_delete'),
    path('wf_edit/<int:pk>/',views.wf_edit,name='wf_edit'),

    # Men Footwear URL
    path('add_men_footwear/',views.add_men_footwear,name='add_men_footwear'),
    path('view_m_sandals/',views.view_m_sandals,name='view_m_sandals'),
    path('view_m_flipflop/',views.view_m_flipflop,name='view_m_flipflop'),
    path('view_m_canvas_shoes/',views.view_m_canvas_shoes,name='view_m_canvas_shoes'),
    path('view_brogues/',views.view_brogues,name='view_brogues'),
    path('view_oxford/',views.view_oxford,name='view_oxford'),
    path('view_loafers/',views.view_loafers,name='view_loafers'),
    path('view_m_sport_shoes/',views.view_m_sport_shoes,name='view_m_sport_shoes'),
    path('view_leather/',views.view_leather,name='view_leather'),
    path('mf_product_detail/<int:pk>/',views.mf_product_detail,name='mf_product_detail'),
    path('mf_stock_avaibility/<int:pk>/',views.mf_stock_avaibility,name='mf_stock_avaibility'),
    path('mf_delete/<int:pk>/',views.mf_delete,name='mf_delete'),
    path('mf_edit/<int:pk>/',views.mf_edit,name='mf_edit'),

    path('search_item/',views.search_item,name='search_item'),

    # Buyer Side URL
    path('show_w_cloths/<str:cn>/',views.show_w_cloths,name='show_w_cloths'),
    path('user_wc_detail/<int:pk>/',views.user_wc_detail,name='user_wc_detail'),
    # path('show_stock_avaibility/<int:pk>/',views.wc_stock_avaibility,name='wc_stock_avaibility'),

    path('show_m_cloths/<str:sc>/',views.show_m_cloths,name='show_m_cloths'),
    path('user_mc_detail/<int:pk>/',views.user_mc_detail,name='user_mc_detail'),
    # path('show_m_stock_avaibility/<int:pk>/',views.wc_stock_avaibility,name='wc_stock_avaibility'),

    path('show_w_acc/<str:sa>/',views.show_w_acc,name='show_w_acc'),
    path('user_wa_detail/<int:pk>/',views.user_wa_detail,name='user_wa_detail'),
    # path('show_m_stock_avaibility/<int:pk>/',views.wc_stock_avaibility,name='wc_stock_avaibility'),

    path('show_m_acc/<str:sa>/',views.show_m_acc,name='show_m_acc'),
    path('user_ma_detail/<int:pk>/',views.user_ma_detail,name='user_ma_detail'),
    # path('show_m_stock_avaibility/<int:pk>/',views.wc_stock_avaibility,name='wc_stock_avaibility'),

    path('show_w_footwear/<str:sf>/',views.show_w_footwear,name='show_w_footwear'),
    path('user_wf_detail/<int:pk>/',views.user_wf_detail,name='user_wf_detail'),
    # path('show_m_stock_avaibility/<int:pk>/',views.wc_stock_avaibility,name='wc_stock_avaibility'),

    path('show_m_footwear/<str:sf>/',views.show_m_footwear,name='show_m_footwear'),
    path('user_mf_detail/<int:pk>/',views.user_mf_detail,name='user_mf_detail'),
    # path('show_m_stock_avaibility/<int:pk>/',views.wc_stock_avaibility,name='wc_stock_avaibility'),

    # Wishlist URL
    path('mywishlist/',views.mywishlist,name='mywishlist'),
    path('add_to_wishlist/<int:pk>/<str:t>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('remove_from_wishlist/<int:pk>/<str:x>/',views.remove_from_wishlist,name='remove_from_wishlist'),
    path('move_to_wishlist/<int:pk>/<str:l>/',views.move_to_wishlist,name='move_to_wishlist'),

    # Cart URL
    path('mycart/',views.mycart,name='mycart'),
    path('add_to_cart/<int:pk>/<str:s>/',views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:pk>/<str:y>/',views.remove_from_cart,name='remove_from_cart'),
    path('move_to_cart/<int:pk>/<str:k>/',views.move_to_cart,name='move_to_cart'),
    path('update_price/',views.update_price,name='update_price'),

    path('checkout_/',views.checkout_,name='checkout_'),
    path('checkout/',views.checkout,name='checkout'),

    path('pay/',views.initiate_payment, name='pay'),
    path('callback/',views.callback, name='callback'),

    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
]