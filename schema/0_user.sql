-- auto-generated definition
create table `0_user`
(
    id           int auto_increment
        primary key,
    user_id      int                                                                               not null,
    label        enum ('happiness', 'sadness', 'neutral', 'disgust', 'fear', 'anger', 'surprised') null,
    happiness    double                                                                            not null,
    sadness      double                                                                            not null,
    neutral      double                                                                            not null,
    disgust      double                                                                            not null,
    fear         double                                                                            not null,
    anger        double                                                                            not null,
    surprised    double                                                                            not null,
    music_id     int                                                                               not null,
    is_satisfied tinyint                                                                           not null,
    log_at       timestamp default CURRENT_TIMESTAMP                                               not null
);


