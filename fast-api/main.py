from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uvicorn

app = FastAPI(title="Mock API Service", description="包含模拟测试数据的API服务", version="1.0.0")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class User(BaseModel):
    id: int
    name: str
    email: str
    age: int
    city: str
    created_at: str

class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str
    stock: int
    description: str

class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total: float
    status: str
    order_date: str

# 模拟测试数据
mock_users = [
    User(id=1, name="张三", email="zhangsan@example.com", age=28, city="北京", created_at="2024-01-15"),
    User(id=2, name="李四", email="lisi@example.com", age=32, city="上海", created_at="2024-01-20"),
    User(id=3, name="王五", email="wangwu@example.com", age=25, city="深圳", created_at="2024-02-01"),
    User(id=4, name="赵六", email="zhaoliu@example.com", age=29, city="广州", created_at="2024-02-10"),
    User(id=5, name="钱七", email="qianqi@example.com", age=35, city="杭州", created_at="2024-02-15"),
]

mock_products = [
    Product(id=1, name="iPhone 15", price=6999.0, category="电子产品", stock=50, description="最新款苹果手机"),
    Product(id=2, name="MacBook Pro", price=12999.0, category="电子产品", stock=30, description="专业级笔记本电脑"),
    Product(id=3, name="Nike Air Max", price=899.0, category="运动鞋", stock=100, description="经典运动鞋款"),
    Product(id=4, name="Python编程书", price=89.0, category="图书", stock=200, description="Python学习必备"),
    Product(id=5, name="咖啡豆", price=128.0, category="食品", stock=80, description="精品蓝山咖啡豆"),
]

mock_orders = [
    Order(id=1, user_id=1, product_id=1, quantity=1, total=6999.0, status="已完成", order_date="2024-03-01"),
    Order(id=2, user_id=2, product_id=3, quantity=2, total=1798.0, status="配送中", order_date="2024-03-05"),
    Order(id=3, user_id=3, product_id=4, quantity=3, total=267.0, status="已完成", order_date="2024-03-10"),
    Order(id=4, user_id=1, product_id=5, quantity=2, total=256.0, status="处理中", order_date="2024-03-15"),
    Order(id=5, user_id=4, product_id=2, quantity=1, total=12999.0, status="已完成", order_date="2024-03-20"),
]

# API 路由
@app.get("/")
def root():
    return {
        "message": "欢迎使用模拟API服务",
        "endpoints": {
            "用户": "/users",
            "产品": "/products", 
            "订单": "/orders",
            "API文档": "/docs"
        }
    }

# 用户相关API
@app.get("/users", response_model=List[User])
def get_users():
    """获取所有用户"""
    return mock_users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    """根据ID获取用户"""
    user = next((u for u in mock_users if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@app.get("/users/city/{city}")
def get_users_by_city(city: str):
    """根据城市获取用户"""
    users = [u for u in mock_users if u.city == city]
    return {"city": city, "users": users, "count": len(users)}

# 产品相关API
@app.get("/products", response_model=List[Product])
def get_products():
    """获取所有产品"""
    return mock_products

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    """根据ID获取产品"""
    product = next((p for p in mock_products if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    return product

@app.get("/products/category/{category}")
def get_products_by_category(category: str):
    """根据分类获取产品"""
    products = [p for p in mock_products if p.category == category]
    return {"category": category, "products": products, "count": len(products)}

# 订单相关API
@app.get("/orders", response_model=List[Order])
def get_orders():
    """获取所有订单"""
    return mock_orders

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    """根据ID获取订单"""
    order = next((o for o in mock_orders if o.id == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return order

@app.get("/orders/user/{user_id}")
def get_orders_by_user(user_id: int):
    """根据用户ID获取订单"""
    orders = [o for o in mock_orders if o.user_id == user_id]
    return {"user_id": user_id, "orders": orders, "count": len(orders)}

@app.get("/orders/status/{status}")
def get_orders_by_status(status: str):
    """根据状态获取订单"""
    orders = [o for o in mock_orders if o.status == status]
    return {"status": status, "orders": orders, "count": len(orders)}

# 统计API
@app.get("/stats")
def get_stats():
    """获取统计信息"""
    total_revenue = sum(o.total for o in mock_orders if o.status == "已完成")
    return {
        "用户总数": len(mock_users),
        "产品总数": len(mock_products),
        "订单总数": len(mock_orders),
        "总收入": total_revenue,
        "平均订单金额": round(total_revenue / len([o for o in mock_orders if o.status == "已完成"]), 2)
    }

# 健康检查
@app.get("/health")
def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)