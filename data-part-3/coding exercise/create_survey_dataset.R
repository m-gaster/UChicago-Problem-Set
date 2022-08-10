# produce dataset of "matched" arrests for survey

# create basic arrest data
arrest_data <- read_csv("data/clean/temp/arrest.csv")
prisoner_data <- read_csv("data/clean/temp/prisoner.csv")
arrest_data <- arrest_data %>% left_join(prisoner_data, by = c("prisoner_id"))

# method A: loop over arrests
arrest_pairs_a <- tibble()
while(nrow(arrest_pairs_a) < 100) {
  # get LHS arrest
  arrest_left <- arrest_data %>% slice_sample(n = 1)

  # get potential matches
  arrest_matches <- arrest_data %>%
    filter(
      release_flag != arrest_left$release_flag,
      sex == arrest_left$sex,
      race == arrest_left$race
    )

  # add pair to final dataset
  if(nrow(arrest_matches) > 0) {
    arrest_match <- arrest_matches %>% slice_sample(n = 1)
    arrest_pair <- tibble(
      "arrest_id_left" = arrest_left$arrest_id,
      "prisoner_id_left" = arrest_left$prisoner_id,
      "arrest_id_right" = arrest_left$arrest_id,
      "prisoner_id_right" = arrest_left$prisoner_id
    )
    arrest_pairs_a <- bind_rows(arrest_pairs_a, arrest_pair)
  }
}

# method B: cross-join all arrests
arrest_pairs_b <- inner_join(
  arrest_data %>% filter(release_flag == 0) %>% select(arrest_id, prisoner_id, race, sex),
  arrest_data %>% filter(release_flag == 1) %>% select(arrest_id, prisoner_id, race, sex),
  by = c("race", "sex"),
  suffix = c("_left", "_right")
) %>%
  select(-race, -sex) %>%
  slice_sample(n = 100)
