#!/usr/bin/env python3
"""
Test the coupon code fix
"""

from udemypy.course import Course
from datetime import datetime

def test_coupon_fix():
    """Test the coupon code fix"""
    
    print("🧪 Testing Coupon Code Fix")
    print("=" * 50)
    
    # Test case 1: Link without coupon code
    course1 = Course(
        id=1,
        title="Test Course 1",
        link="https://www.udemy.com/course/test-course/",
        coupon_code="TEST123",
        date_found=datetime.now()
    )
    
    print(f"Test 1 - Link without coupon:")
    print(f"  Original link: {course1.link}")
    print(f"  Coupon code: {course1.coupon_code}")
    print(f"  Link with coupon: {course1.link_with_coupon}")
    print()
    
    # Test case 2: Link with coupon code already included
    course2 = Course(
        id=2,
        title="Test Course 2",
        link="https://www.udemy.com/course/test-course/?couponCode=EXISTING123",
        coupon_code="NEW456",
        date_found=datetime.now()
    )
    
    print(f"Test 2 - Link with existing coupon:")
    print(f"  Original link: {course2.link}")
    print(f"  Coupon code: {course2.coupon_code}")
    print(f"  Link with coupon: {course2.link_with_coupon}")
    print()
    
    # Test case 3: Real example from your issue
    course3 = Course(
        id=3,
        title="Advanced Certified Scrum Master",
        link="https://www.udemy.com/course/advanced-certified-scrum-master/?couponCode=FCF5A6FCDFEC4CF4E2AF",
        coupon_code="FCF5A6FCDFEC4CF4E2AF",
        date_found=datetime.now()
    )
    
    print(f"Test 3 - Real example:")
    print(f"  Original link: {course3.link}")
    print(f"  Coupon code: {course3.coupon_code}")
    print(f"  Link with coupon: {course3.link_with_coupon}")
    print()
    
    print("✅ Coupon code fix test completed!")


if __name__ == "__main__":
    test_coupon_fix() 