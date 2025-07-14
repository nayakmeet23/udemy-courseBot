SELECT c.id,
	c.title,
    c.link,
    c.coupon_code,
    c.date_found,
    c.discount_time_left, 
    c.students,
    c.rating,
    c.language,
    c.badge
FROM
    course AS c,
    course_social_media AS csm,
    social_media as sm
WHERE c.id = csm.course_id
    AND csm.social_media_id = sm.id
    AND sm.name = "Twitter";