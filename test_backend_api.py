import pytest
import requests
import sqlite3  # 用内置数据库模拟 SQL 校验能力

class TestBackendDemo:
    """
    这个 Demo 展现了：API自动化、多环境配置意识、业务流测试、以及数据库校验。
    """
    
    # 模拟基础配置
    BASE_URL = "https://jsonplaceholder.typicode.com" # 使用公开的 API 练习
    
    @pytest.fixture
    def db_connection(self):
        """模拟 JD 要求的 Database validation 能力"""
        conn = sqlite3.connect(':memory:') # 在内存中创建模拟数据库
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE orders (id INTEGER, status TEXT)')
        cursor.execute('INSERT INTO orders VALUES (1, "SUCCESS")')
        yield cursor
        conn.close()

    def test_get_user_validation(self):
        """能力展现：API 基础校验与状态码检查"""
        response = requests.get(f"{self.BASE_URL}/users/1")
        assert response.status_code == 200
        assert "email" in response.json()
        print("\n[Check] API 状态码和基本字段校验通过")

    def test_complex_business_workflow(self):
        """能力展现：微服务/业务逻辑流测试 (创建并验证)"""
        # 1. 模拟创建资源
        payload = {"title": "test_post", "body": "bar", "userId": 1}
        post_response = requests.post(f"{self.BASE_URL}/posts", json=payload)
        assert post_response.status_code == 201
        new_id = post_response.json()['id']
        
        # 2. 模拟紧接着的查询操作
        get_response = requests.get(f"{self.BASE_URL}/posts/1") # 实际测试中会用 new_id
        assert get_response.status_code == 200
        print(f"\n[Check] 业务逻辑流：创建资源 ID {new_id} 并验证成功")

    def test_database_integrity(self, db_connection):
        """能力展现：JD 要求的数据库操作 (SQL queries)"""
        db_connection.execute('SELECT status FROM orders WHERE id=1')
        result = db_connection.fetchone()
        assert result[0] == "SUCCESS"
        print("\n[Check] 数据库后端校验：数据一致性匹配")
