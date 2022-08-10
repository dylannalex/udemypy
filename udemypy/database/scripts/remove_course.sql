DELETE c, csm FROM 
    course AS c,
    course_social_media AS csm
WHERE c.id = id_value
    AND c.id = csm.course_id;